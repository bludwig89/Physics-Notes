# Visualization design — the dump/render seam and the renderer options

*Created 2026-07-29 - 21:05*

Companion to `docs/roadmaps/roadmap-unified-program.md` §P5 (the GUI as a
workbench). P5.1 consolidates the three duplicate viz generations; this document
answers the prior question — *what should the renderer be, and does the model
need a 3-D one at all* — and records the seam that makes the answer replaceable.

---

## 1. Does the model need a 3-D visualizer?

**Mostly no.** Nearly every claim this project makes is spectral or algebraic:
ω(k) dispersion residuals, PPN β = γ = 1, b₀ = 11/3·C_A, the Koide chain,
√σ/f_π, δ* = 2/9. A volume render cannot confirm or refute any of them. A 1-D
plot of ω(k) against the analytic curve with a residual panel carries more
information than any 3-D scene, and the JSON result dumps carry more than both.
Numeric output plus matplotlib residual figures stay the primary product.

Three-dimensional rendering earns its cost in four places, all of them
*spatial-structure* questions where the answer is a shape rather than a number:

| Use | Why numerics are insufficient |
|-----|-------------------------------|
| Real-space runs (F134–F137, the unified one-lattice arc) | Whether a bag forms and stays bound is a topological fact about a region, not a scalar |
| Flux tubes / colour dielectric (F86, F142) | Confinement claims are about whether a tube *exists*; a spreading blob and a tube can have similar integrated observables |
| Interior/exterior metric structure (F178, F181) | Largely covered by radial line plots — 3-D is a convenience here, not a requirement |
| Debugging | Doublers, boundary reflection, and CFL blow-up are visually obvious and numerically subtle |

The corollary that matters for cost: the live 3-D view is a *debugging and
intuition* instrument, not a measurement instrument. It is therefore allowed to
be approximate, and it must never slow the physics down.

---

## 2. The seam: dump, don't couple

The decision recorded here is that **the engine never imports a renderer.**
It writes real scalar/vector volumes to disk, and any frontend reads them.

Implemented as `casim.io.vtk` (a dependency-free VTK XML ImageData + Collection
writer) driven by the `field_dump` observer:

```yaml
observers:
  - {type: field_dump, every: 10, format: vti, stride: 2, max_mb: 256}
```

This yields `test-results/fields/<run>/<channel>_t000010.vti` per tick per
channel plus a `<channel>.pvd` collection that loads the whole run as a ParaView
time series. `format: npz` gives the same volumes for numpy/napari consumers;
`components: true` adds the raw fields alongside the density.

Four properties this buys, in order of importance:

1. **The physics path acquires no GUI dependency.** VTK ImageData is a short XML
   header plus raw little-endian binary; writing it costs ~100 lines and no
   third-party package. ParaView, PyVista, napari, and `vtk`-Python all read the
   result.
2. **Long native runs stay inspectable after the fact** — the same motivation as
   checkpoint/resume, and the reason a run that takes hours on Apple Silicon
   does not also have to hold a window open.
3. **Renderer choice becomes reversible.** Nothing downstream of the dump is
   load-bearing, so trying napari and abandoning it costs nothing.
4. **Complex truncation becomes explicit.** The writer *refuses* complex arrays;
   the observer splits them into named `f_re`/`f_im` volumes. A renderer that
   silently drops Im(ψ) produces a picture that looks fine and is wrong — the
   same failure mode CLAUDE.md warns about for numpy/scipy chiral transforms.

Two caveats are recorded in the output metadata rather than left implicit:

- **ImageData is a uniform grid.** A BCC lattice stored as an (L,L,L) array is
  written with cubic indexing. This is exact for every array-indexed field the
  engine holds, but the geometric BCC sublattice offsets are not applied.
  `topology` travels in the sidecar so a consumer can apply them.
- **VTK point order is x-fastest** (`p = ix + nx*(iy + ny*iz)`), the opposite of
  numpy C order. Every array is raveled `order="F"`. Dropping that ravel renders
  a transposed volume that looks plausible; `tests/casim/test_field_dump_vtk.py`
  asserts the index formula longhand so the test cannot pass by agreeing with
  the writer's own ravel.

---

## 3. Renderer options, by cost

### 3.1 What the current vispy view actually spends

`casim.gui.render.point_cloud` runs, per frame per visible channel, over the
full L³ volume:

1. `np.abs(density)` — a full-volume copy. The input is already non-negative
   (`density_field` returns |ψ|² or E²+B²), so this pass buys nothing.
2. `np.percentile(flat, pctile)` — a **full sort**, O(n log n), on every frame.
   Only above 2²² voxels does it fall back to a strided sample.
3. `mask`, `np.argwhere` → a fresh (M,3) array, and `tinted_rgba` → a fresh
   (M,4) array. Both reallocated every frame, then uploaded to the GPU whole.

At L = 64 that is ~262k voxels and ~5 full-volume passes plus a sort per frame;
at L = 128 it is 2.1M voxels and the upload dominates. On top of that, PyQt6 +
vispy cost ~150 MB resident before any physics runs.

### 3.2 The options

| Option | Cost | What it is good for |
|--------|------|---------------------|
| **A. Keep vispy, cut the per-frame work** | ~0 new deps | The existing 3-D view, made cheap |
| **B. matplotlib slice viewer** | ~30 MB, no GPU | Live debugging — the best ratio in this table |
| **C. Headless PNG/heatmap per N ticks** | ~0 | Long native runs, scriptable figures |
| **D. Browser viewer over the dump** | no Qt | Sharing; killing the viewer without touching the sim |
| **E. Offline in ParaView / napari / PyVista** | 0 during the run | Everything else — now enabled by §2 |

**A — keep vispy, cut the work.** Four changes, all local to `render.py` and
`app.py`, none touching physics:

- Drop the `np.abs` pass; assert non-negativity in the channel contract instead.
- Replace `np.percentile` with `np.partition`/`argpartition` for a **fixed
  point budget** (top-M voxels) rather than a percentile. O(n) instead of a
  sort, and the GPU upload becomes bounded regardless of L.
- Always estimate the threshold on a strided sample. The docstring already
  concedes the threshold is "a visual cut, not a physics quantity", so the
  approximation is licensed at every size, not just above 2²².
- Preallocate the coords/colour buffers at the point budget and fill in place;
  decouple frame rate from step rate (`steps_per_frame` is hard-coded to 2 at
  `app.py:170`).

Longer-term, upload the density as a 3-D texture once per frame and colour-map
in the fragment shader, so no (M,4) float32 array is built in numpy at all.

**B — matplotlib slice viewer (the recommendation for routine debugging).**
Three orthogonal mid-plane slices (xy / xz / yz) with `imshow` and `set_data` on
a timer. ~50 lines, no GPU, no Qt, and for the things actually being debugged —
packet spread, bag formation, boundary reflection, doubler contamination — a
slice is *more* legible than a thresholded point cloud, because a point cloud
hides interior structure behind its own surface. This is §1's conclusion applied
to the live view.

**C — headless.** `tick_heatmap.py` already does this for the tick field N(x);
generalising it to any channel's `density_field` at a tick cadence gives
scriptable figures with no interactive cost. The natural home is `casim.viz`,
which P5.1 wants to fill with a real static-figure layer.

**D — browser.** With the dump in place, a small HTML page (three.js, or
`itk-vtk-viewer` reading the `.vti` directly) removes PyQt6 entirely and runs the
renderer in a process that can be killed independently of the simulation.

**E — offline.** ParaView already solves the hard parts — level of detail, large
data, remote rendering, animation, publication-quality output. Building a custom
3-D engine would be rewriting it. Since §2 landed, this is free.

### 3.3 Not recommended

- **pyqtgraph** — still a Qt dependency; no saving over fixing A.
- **vedo / PyVista as the *live* renderer** — both pull in full VTK (~135 MB
  wheel), heavier than vispy, not lighter. Excellent offline (E), wrong for a
  live loop.
- **A custom 3-D engine** — see E.

---

## 4. Decision

1. **Offline-first.** `field_dump` + ParaView/PyVista/napari is the primary 3-D
   path. The engine stays renderer-free.
2. **Keep vispy for live stepping**, with the §3.2-A fixes; it is built, working,
   and undersold.
3. **Add the matplotlib slice viewer** as the low-cost default debug view, and
   give `casim.viz` the static-figure layer P5.1 asks for.
4. **Never reduce a complex field for a renderer implicitly.** Reduce to named
   real observables at the dump boundary, where it is auditable.

---

*Cross-references: `docs/roadmaps/roadmap-unified-program.md` §P5, §P6;
`src/casim/io/vtk.py`; `src/casim/engine/observers.py` (`FieldDump`);
`tests/casim/test_field_dump_vtk.py`; `src/casim/gui/render.py`.*
