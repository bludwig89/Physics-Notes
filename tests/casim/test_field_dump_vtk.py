"""Tests for the visualisation seam: casim.io.vtk + the field_dump observer.

The writer is hand-rolled (no VTK dependency on the physics path), so the two
things that can silently go wrong are asserted directly against the bytes:

  1. **Point ordering.**  VTK indexes points ``p = ix + nx*(iy + ny*iz)`` —
     x fastest — while numpy C order runs z fastest.  If the ``order="F"``
     ravel is ever dropped, volumes render transposed: a plausible-looking,
     wrong picture.  Tested by decoding the appended block and comparing to
     an explicit index formula, not to another numpy ravel.
  2. **Complex handling.**  A renderer that drops Im(psi) also produces a
     plausible wrong picture.  The writer must *refuse* complex input, and the
     observer must split it into explicitly named re/im volumes.

Everything here is pure numpy — no VTK, no vispy, no Qt — so it runs headless.
"""
from __future__ import annotations

import re
import struct

import numpy as np
import pytest

from casim.engine.core.observers import build_observer
from casim.io.vtk import write_image_data, write_pvd


# ----------------------------------------------------------------------
# Helpers: read back a .vti without a VTK dependency
# ----------------------------------------------------------------------
def _read_vti(path):
    """Return (header_str, [np.ndarray, ...]) decoded from the appended block."""
    raw = open(path, "rb").read()
    start = raw.index(b'<AppendedData encoding="raw">')
    marker = raw.index(b"_", start) + 1      # the '_' *after* the tag, not the
    header = raw[:marker].decode("ascii")    # one inside byte_order/header_type
    kinds = {"Float32": "<f4", "Float64": "<f8"}
    decls = re.findall(
        r'type="(\w+)" Name="(\w+)" NumberOfComponents="(\d+)"', header)
    out, off = [], marker
    for vtype, name, ncomp in decls:
        nbytes = struct.unpack("<Q", raw[off:off + 8])[0]
        off += 8
        a = np.frombuffer(raw[off:off + nbytes], dtype=kinds[vtype])
        off += nbytes
        out.append((name, int(ncomp), a))
    return header, out


# ----------------------------------------------------------------------
# 1. Point ordering — the transpose bug
# ----------------------------------------------------------------------
def test_point_order_is_x_fastest(tmp_path):
    nx, ny, nz = 4, 5, 6
    a = np.arange(nx * ny * nz, dtype=np.float64).reshape(nx, ny, nz)
    path = write_image_data(str(tmp_path / "s.vti"), {"density": a},
                            dtype=np.float64)
    header, arrays = _read_vti(path)

    assert f'WholeExtent="0 {nx-1} 0 {ny-1} 0 {nz-1}"' in header
    (name, ncomp, flat), = arrays
    assert (name, ncomp) == ("density", 1)

    # Compare against the VTK index formula written out longhand, so this test
    # cannot pass by agreeing with the same ravel the writer uses.
    for ix, iy, iz in [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
                       (3, 4, 5), (2, 3, 1)]:
        p = ix + nx * (iy + ny * iz)
        assert flat[p] == a[ix, iy, iz], (ix, iy, iz)


def test_vector_components_are_interleaved(tmp_path):
    nx, ny, nz = 3, 4, 5
    a = np.arange(nx * ny * nz, dtype=np.float64).reshape(nx, ny, nz)
    vec = np.stack([a, a + 1000.0, a + 2000.0])       # (3, nx, ny, nz)
    path = write_image_data(str(tmp_path / "v.vti"), {"E": vec},
                            dtype=np.float64)
    _, ((name, ncomp, flat),) = _read_vti(path)
    assert (name, ncomp) == ("E", 3)
    tup = flat.reshape(-1, 3)
    for ix, iy, iz in [(0, 0, 0), (2, 1, 3), (1, 3, 4)]:
        p = ix + nx * (iy + ny * iz)
        assert tup[p, 0] == a[ix, iy, iz]
        assert tup[p, 1] == a[ix, iy, iz] + 1000.0
        assert tup[p, 2] == a[ix, iy, iz] + 2000.0


def test_mismatched_grids_are_rejected(tmp_path):
    with pytest.raises(ValueError):
        write_image_data(str(tmp_path / "bad.vti"),
                         {"a": np.zeros((4, 4, 4)), "b": np.zeros((4, 4, 5))})


# ----------------------------------------------------------------------
# 2. Complex handling — the silent-truncation bug
# ----------------------------------------------------------------------
def test_writer_refuses_complex(tmp_path):
    z = np.ones((3, 3, 3), dtype=np.complex128)
    with pytest.raises(TypeError, match="complex"):
        write_image_data(str(tmp_path / "z.vti"), {"psi": z})


def test_observer_splits_complex_into_named_re_im():
    """A complex spinor must surface as f_re/f_im, never as a bare truncation."""
    class _Ch:
        def density_field(self, st):
            return np.abs(st["f"]) ** 2 + np.abs(st["g"]) ** 2

    f = (np.arange(8).reshape(2, 2, 2) + 1j * np.arange(8, 16).reshape(2, 2, 2))
    g = np.zeros((2, 2, 2), dtype=complex)
    obs = build_observer({"type": "field_dump"})
    arrays = obs._real_arrays(_Ch(), {"f": f, "g": g}, components=True)

    assert set(arrays) >= {"density", "f_re", "f_im", "g_re", "g_im"}
    assert np.array_equal(arrays["f_re"], f.real)
    assert np.array_equal(arrays["f_im"], f.imag)
    assert not any(np.iscomplexobj(v) for v in arrays.values())


# ----------------------------------------------------------------------
# 3. Observer integration
# ----------------------------------------------------------------------
def test_field_dump_writes_series_and_collection(tmp_path):
    """End-to-end on the Weyl BCC channel: files per tick + a .pvd index."""
    from casim.engine import Simulation

    scenario = {
        "name": "dump_smoke",
        "lattice": {"L": 8, "topology": "bcc"},
        "seed": 0,
        "ticks": 4,
        "channels": [{"type": "weyl_bcc", "name": "psi"}],
        "observers": [{"type": "field_dump", "every": 2,
                       "dir": str(tmp_path), "format": "vti"}],
    }
    sim = Simulation.from_scenario(scenario)
    results = sim.run(4)
    summary = results["observers"]["field_dump"]["summary"]

    assert summary["files_written"] == 3          # ticks 0, 2, 4
    assert "psi" in summary["collections"]
    assert not summary["skipped_channels"]

    pvd = open(summary["collections"]["psi"]).read()
    for tick in (0, 2, 4):
        assert f"psi_t{tick:06d}.vti" in pvd
    # timesteps must be ordered so ParaView animates forward
    times = [float(t) for t in re.findall(r'timestep="([\d.]+)"', pvd)]
    assert times == sorted(times) == [0.0, 2.0, 4.0]

    header, arrays = _read_vti(str(tmp_path / "psi_t000000.vti"))
    assert [n for n, _, _ in arrays] == ["density"]
    assert 'Name="tick"' in header                # FieldData metadata survives


def test_field_dump_skips_channels_without_a_volume(tmp_path):
    """Compute-once / register channels must be skipped, not crash the run."""
    class _NoVolume:
        def density_field(self, st):
            raise ValueError("no spatial density field")

    obs = build_observer({"type": "field_dump", "dir": str(tmp_path)})
    with pytest.raises(ValueError):
        obs._real_arrays(_NoVolume(), {}, components=False)


def test_stride_downsamples_all_shapes():
    obs = build_observer({"type": "field_dump"})
    scalar = np.zeros((8, 8, 8))
    vector = np.zeros((3, 8, 8, 8))
    assert obs._stride(scalar, 2).shape == (4, 4, 4)
    assert obs._stride(vector, 2).shape == (3, 4, 4, 4)
    assert obs._stride(scalar, 1).shape == (8, 8, 8)


def test_pvd_roundtrip(tmp_path):
    path = write_pvd(str(tmp_path / "c.pvd"), [(0.0, "a.vti"), (1.0, "b.vti")])
    text = open(path).read()
    assert 'type="Collection"' in text
    assert text.count("<DataSet") == 2
