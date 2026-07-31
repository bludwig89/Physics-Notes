"""casim.io.vtk — dependency-free VTK XML writers (ImageData + Collection).

Why hand-rolled: the repo's standing rule is that nothing in the physics path
acquires a heavy dependency, and the visualisation seam must not be an
exception (see ``docs/design/visualization.md``).  A ``.vti`` file is a short
XML header followed by raw little-endian binary, so writing one costs ~100
lines and buys ParaView, PyVista, napari, and VTK-Python readers for free.
The simulation therefore never imports a renderer: it dumps, and any frontend
reads.

Layout written here: **VTKFile/ImageData, appended raw, UInt64 headers,
LittleEndian.**  One ``<DataArray>`` per named field, all point data.

Ordering caveat (the easy bug): VTK point index is
``p = ix + nx*(iy + ny*iz)`` — *x fastest*.  Our arrays are indexed
``a[ix, iy, iz]`` in C order (z fastest), so every array is flattened with
``order="F"`` to swap the convention.  Get this wrong and the volume renders
transposed, which looks plausible and is therefore dangerous.

Complex caveat: VTK has no complex type.  Nothing here accepts a complex
array — callers must reduce to real observables (|ψ|², Re, Im) *before*
writing, so the reduction is explicit and auditable rather than a silent
truncation inside a renderer (CLAUDE.md: numpy/scipy chiral transforms are not
to be trusted to preserve real/imag parts).

Topology caveat: ``ImageData`` is a uniform rectilinear grid.  A BCC lattice
stored as an (L, L, L) array of cells is written as if cubic — correct for
every array-indexed field the engine holds, but the *geometric* BCC offsets are
not represented.  ``topology`` is recorded in the sidecar metadata so a
downstream consumer can apply the offsets if it needs true geometry.
"""
from __future__ import annotations

import os
import struct
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import numpy as np

__all__ = [
    "write_image_data",
    "write_pvd",
    "vtk_dtype_name",
]

#: numpy dtype → VTK type string (real types only; complex is rejected upstream)
_VTK_TYPES = {
    "float32": "Float32",
    "float64": "Float64",
    "int8": "Int8",
    "int16": "Int16",
    "int32": "Int32",
    "int64": "Int64",
    "uint8": "UInt8",
}


def vtk_dtype_name(dtype: np.dtype) -> str:
    """Return the VTK type string for ``dtype``; raise on anything complex."""
    name = np.dtype(dtype).name
    if name.startswith("complex"):
        raise TypeError(
            "complex arrays cannot be written to VTK; reduce to a real "
            "observable (|psi|^2, Re, Im) before dumping"
        )
    try:
        return _VTK_TYPES[name]
    except KeyError:
        raise TypeError(f"unsupported dtype for VTK: {name}")


# ----------------------------------------------------------------------
# Array flattening (the x-fastest convention)
# ----------------------------------------------------------------------
def _as_point_payload(a: np.ndarray) -> Tuple[np.ndarray, int, Tuple[int, int, int]]:
    """Flatten ``a`` to VTK point order; return (flat, n_components, (nx,ny,nz)).

    Accepted shapes
    ---------------
    ``(nx, ny, nz)``        → scalar field, 1 component
    ``(nx, ny)``            → scalar field on a 2-D lattice (nz = 1)
    ``(C, nx, ny, nz)``     → C-component vector/tensor field

    A 3-D array is always read as a 3-D scalar field, never as a component
    stack on a 2-D lattice — the two are indistinguishable from shape alone,
    so a caller wanting the latter must split the components itself and pass
    them under separate names.

    Point ordering is x-fastest, so spatial axes are raveled ``order="F"``;
    components are interleaved per point, which is what VTK expects for a
    multi-component ``DataArray``.
    """
    a = np.asarray(a)
    if np.iscomplexobj(a):
        raise TypeError(
            "complex array reached the VTK writer; reduce to a real "
            "observable before dumping"
        )

    if a.ndim in (2, 3):
        ncomp = 1
        spatial = a
        comps: List[np.ndarray] = [a]
    elif a.ndim == 4:
        ncomp = int(a.shape[0])
        spatial = a[0]
        comps = [a[c] for c in range(ncomp)]
    else:
        raise ValueError(f"cannot write array of shape {a.shape} as point data")

    if spatial.ndim == 2:
        nx, ny = spatial.shape
        nz = 1
    else:
        nx, ny, nz = spatial.shape

    flat = np.stack([np.ascontiguousarray(c).ravel(order="F") for c in comps],
                    axis=1).ravel()
    return flat, ncomp, (int(nx), int(ny), int(nz))


# ----------------------------------------------------------------------
# .vti writer
# ----------------------------------------------------------------------
def write_image_data(path: str,
                     arrays: Dict[str, np.ndarray],
                     spacing: Sequence[float] = (1.0, 1.0, 1.0),
                     origin: Sequence[float] = (0.0, 0.0, 0.0),
                     dtype: Any = np.float32,
                     field_data: Dict[str, float] | None = None) -> str:
    """Write ``arrays`` as one VTK ImageData (``.vti``) file; return abs path.

    Parameters
    ----------
    arrays
        ``{name: ndarray}``.  Every array must describe the *same* lattice
        (see :func:`_as_point_payload` for accepted shapes).  Names become the
        field names in ParaView / PyVista / napari.
    spacing, origin
        Uniform grid geometry.  Defaults are lattice units (1 cell = 1 unit).
    dtype
        Storage dtype; ``float32`` by default, which halves file size and is
        well past what any renderer resolves.  Pass ``np.float64`` when the
        dump is being used for numerical comparison rather than for viewing.
    field_data
        Optional scalar metadata (tick, energy, c_lat, …) written as VTK
        FieldData so it survives into ParaView's information panel.
    """
    if not arrays:
        raise ValueError("write_image_data called with no arrays")

    payloads: List[Tuple[str, np.ndarray, int]] = []
    dims: Tuple[int, int, int] | None = None
    for name, a in arrays.items():
        flat, ncomp, d = _as_point_payload(a)
        if dims is None:
            dims = d
        elif d != dims:
            raise ValueError(
                f"array {name!r} has lattice shape {d}, expected {dims}; "
                "all arrays in one .vti must share a grid"
            )
        payloads.append((name, np.ascontiguousarray(flat, dtype=dtype), ncomp))

    assert dims is not None
    nx, ny, nz = dims
    extent = f"0 {nx - 1} 0 {ny - 1} 0 {nz - 1}"
    vtk_type = vtk_dtype_name(np.dtype(dtype))
    itemsize = np.dtype(dtype).itemsize

    # --- header: compute appended-data offsets (8-byte UInt64 length prefix) --
    offsets: List[int] = []
    running = 0
    for _, flat, _ in payloads:
        offsets.append(running)
        running += 8 + flat.size * itemsize

    scalars = payloads[0][0]
    lines: List[str] = [
        '<?xml version="1.0"?>',
        '<VTKFile type="ImageData" version="1.0" '
        'byte_order="LittleEndian" header_type="UInt64">',
        f'  <ImageData WholeExtent="{extent}" '
        f'Origin="{origin[0]} {origin[1]} {origin[2]}" '
        f'Spacing="{spacing[0]} {spacing[1]} {spacing[2]}">',
    ]
    if field_data:
        lines.append("    <FieldData>")
        for k, v in field_data.items():
            lines.append(
                f'      <DataArray type="Float64" Name="{k}" '
                f'NumberOfTuples="1" format="ascii">{float(v)}</DataArray>'
            )
        lines.append("    </FieldData>")
    lines += [
        f'    <Piece Extent="{extent}">',
        f'      <PointData Scalars="{scalars}">',
    ]
    for (name, _, ncomp), off in zip(payloads, offsets):
        lines.append(
            f'        <DataArray type="{vtk_type}" Name="{name}" '
            f'NumberOfComponents="{ncomp}" format="appended" offset="{off}"/>'
        )
    lines += [
        "      </PointData>",
        "    </Piece>",
        "  </ImageData>",
        '  <AppendedData encoding="raw">',
        "   _",
    ]
    header = "\n".join(lines).encode("ascii")

    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(header)
        for _, flat, _ in payloads:
            fh.write(struct.pack("<Q", flat.size * itemsize))
            fh.write(flat.tobytes(order="C"))
        fh.write(b"\n  </AppendedData>\n</VTKFile>\n")
    return os.path.abspath(path)


# ----------------------------------------------------------------------
# .pvd time-series collection
# ----------------------------------------------------------------------
def write_pvd(path: str, entries: Iterable[Tuple[float, str]]) -> str:
    """Write a ParaView ``.pvd`` collection indexing a time series.

    ``entries`` is an iterable of ``(timestep, relative_filename)``.  Opening
    the ``.pvd`` in ParaView loads the whole run as an animation instead of a
    pile of unrelated files.
    """
    lines = [
        '<?xml version="1.0"?>',
        '<VTKFile type="Collection" version="1.0" byte_order="LittleEndian">',
        "  <Collection>",
    ]
    for t, fname in entries:
        lines.append(
            f'    <DataSet timestep="{float(t)}" group="" part="0" '
            f'file="{fname}"/>'
        )
    lines += ["  </Collection>", "</VTKFile>"]
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    return os.path.abspath(path)
