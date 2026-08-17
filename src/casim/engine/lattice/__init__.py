"""casim.engine.lattice — the BCC base layer (D1) and its reference cubic lattice.

Geometry, shells, Brillouin zone, block-spin/multigrid coarse-graining, and the
canonical BCC constructors (F41/F175/F264). The simple-cubic code retained here
is the **continuum-limit regression target**, not a second canonical lattice.
Populated from the legacy flat kernels at roadmap phase C3 (D6).
"""
from __future__ import annotations
