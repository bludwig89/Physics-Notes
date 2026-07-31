# ===== deprecated/code backup =====================================
# source     : ca-simulation/forks/curl_fork_baseline_bcc.py
# migrated   : 2026-07-30 - 16:09
# target     : src/casim/engine/forks/gauge/curl_fork_baseline_bcc.py
# manifest   : docs/design/module-migration-manifest.yaml  (id: curl_fork_baseline_bcc.py)
# stripped   : (nothing)
# reason     : D6 consolidation; no symbols removed
#
# Everything below this header is BYTE-IDENTICAL to the file as it stood
# before migration. Roadmap C0.5 / D10.
# ==================================================================
"""
Fork: BCC BASELINE geometry  (curl-O(k) investigation)
=======================================================
Not a candidate fix — the existing BCC Weyl QCA (Paper 1 Eq. 15,
`ca_bcc.py`), wrapped to the common curl-fork interface so the harness
can run the same diagnostics on it as on the simple-cubic candidate.

Reference outcomes (already established):
  c_lat (small-k)       = 1/√3            (Finding 10, exact algebraic)
  fermion doublers      = 1               (QCA uniqueness, no doubling)
  curl residual scaling = O(k), coeff 1/√6   (Finding 2)
"""
import numpy as np
import ca_bcc as _bcc
from casim.constants import c_lat

GEOMETRY_NAME = "BCC (baseline)"
C_LAT = c_lat


def uvec(kx, ky, kz, sign="+"):
    return _bcc._bcc_uvec(kx, ky, kz, sign=sign)


def dispersion(kx, ky, kz, sign="+"):
    return _bcc.bcc_dispersion(kx, ky, kz, sign=sign)


def unitary(kx, ky, kz, sign="+"):
    return _bcc.bcc_unitary(kx, ky, kz, sign=sign)


def eigenmodes(kx, ky, kz, sign="+"):
    """Return (psi_plus, psi_minus, omega): U·psi_± = e^{∓iω} psi_±, ω≥0."""
    U_ff, U_fg, U_gf, U_gg = _bcc.bcc_unitary(kx, ky, kz, sign=sign)
    M = np.array([[U_ff, U_fg], [U_gf, U_gg]], dtype=complex)
    w, v = np.linalg.eig(M)
    phases = -np.angle(w)
    ip = int(np.argmax(phases))
    im = 1 - ip
    return v[:, ip], v[:, im], float(phases[ip])
