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

GEOMETRY_NAME = "BCC (baseline)"
C_LAT = 1.0 / np.sqrt(3.0)


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
