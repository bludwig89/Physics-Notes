"""F250 — The all-k gauge pole of the dual-spinor (paired) photon.

The F69/F68 paired photon propagates each Fourier mode by the even-law SO(2)
rotation of the real (E,B) pair at rate

    Omega_pair(k) = w+(k/2) + w-(k/2)         (w+- = ca_bcc dispersion),

applied identically in every Cartesian polarisation component.  Per mode the
one-tick evolution is the 2x2 rotation

    M(O) = [[ cosO,  sinO],
            [-sinO,  cosO]] ,   O = Omega_pair(k),

and on the 6-vector field (Ex,Ey,Ez,Bx,By,Bz) it is M6 = M (x) I3 (block form).
The discrete-time propagator is the resolvent G(z,k) = (z I - M6)^{-1},
z = e^{i wfreq}, whose poles are the lattice photon frequencies.

"All-k gauge pole" = for EVERY k in the first Brillouin zone (not merely the
k->0 continuum limit) the propagator has a single simple massless pole at
wfreq = +- Omega_pair(k) whose residue is the transverse (2-polarisation) gauge
projector.  We prove it via 8 grounded checks (closed-form arccos(u) dispersion
+ real linear algebra only; no np.linalg.eig on chiral matrices):

  GP1  Pole location, all k: det(e^{+-iO} I2 - M) = 0 exactly (the rotation's
       eigenvalues are exactly e^{+-iO}), for random k across the full BZ.
  GP2  Massless anchor: Omega_pair(0) = 0 exactly (pure-hop A0=0, F168/B1).
  GP3  Ward / gauge structure: [M6, P_T (x) I2] = 0 (literal 0) — the transverse
       physical subspace is dynamically invariant at every k.
  GP4  Residue is transverse rank 2 (two physical polarisations); the full
       eigenprojector is rank 3; and k . R_T = 0 (Ward identity).
  GP5  Eigenphases from an independent 6x6 diagonalisation equal +-Omega_pair.
  GP6  Unitary (M6 M6^T = I) and spectral completeness P+ + P- = I: residue
       weight 1, no wavefunction renormalisation, no ghost/continuum.
  GP7  SINGLE gauge pole (no doubler): Omega_pair(k) has a unique zero in the
       photon BZ, at k=0.  The k/2 momentum sharing folds the constituent Weyl
       doublers (at the constituent BZ boundary) out to |k|=2pi, outside the
       photon BZ.
  GP8  Independent residue: closed-form projector == eigenvector-built projector.
"""

import json
import os
import sys

import numpy as np

try:
    import pytest
except ModuleNotFoundError:  # allow standalone __main__ JSON dump without pytest
    class _Mark:
        def __getattr__(self, _):
            return lambda f: f

    class _Pytest:
        mark = _Mark()

    pytest = _Pytest()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "ca-simulation"))
from ca_bcc import bcc_dispersion as w  # noqa: E402

RESULT = os.path.join(
    os.path.dirname(__file__), "..", "..", "test-results",
    "F250_allk_gauge_pole.json",
)
ROOT3 = np.sqrt(3.0)
_RNG = np.random.default_rng(20260715)


# ---------------------------------------------------------------- helpers
def Omega(k):
    """Paired-photon rotation rate Omega_pair(k) = w+(k/2) + w-(k/2)."""
    h = np.asarray(k, float) / 2.0
    return float(w(*h, sign="+") + w(*h, sign="-"))


def M2(O):
    c, s = np.cos(O), np.sin(O)
    return np.array([[c, s], [-s, c]])


def M6(O):
    """One-tick evolution on (Ex,Ey,Ez,Bx,By,Bz): M2 (x) I3 (block form)."""
    c, s = np.cos(O), np.sin(O)
    I3 = np.eye(3)
    Z = np.zeros((3, 3))
    return np.block([[c * I3, s * I3], [-s * I3, c * I3]])


def PT6(k):
    """Transverse projector P_T = I - khat khat^T, on both E and B blocks."""
    kh = np.asarray(k, float)
    kh = kh / np.linalg.norm(kh)
    PT = np.eye(3) - np.outer(kh, kh)
    Z = np.zeros((3, 3))
    return np.block([[PT, Z], [Z, PT]])


def _bz_points(n, avoid_origin=False):
    pts = _RNG.uniform(-np.pi, np.pi, size=(n, 3))
    if avoid_origin:
        for i in range(n):
            while np.linalg.norm(pts[i]) < 1e-3:
                pts[i] = _RNG.uniform(-np.pi, np.pi, 3)
    return pts


# ---------------------------------------------------------------- the checks
def _gp1_pole_location(n=4000):
    worst = 0.0
    for k in _bz_points(n):
        O = Omega(k)
        M = M2(O)
        for z in (np.exp(1j * O), np.exp(-1j * O)):
            worst = max(worst, abs(np.linalg.det(z * np.eye(2) - M)))
    return worst


def _gp2_massless_anchor():
    return abs(Omega([0.0, 0.0, 0.0]))


def _gp3_ward_commutator(n=2000):
    worst = 0.0
    for k in _bz_points(n, avoid_origin=True):
        M = M6(Omega(k))
        P = PT6(k)
        worst = max(worst, np.max(np.abs(M @ P - P @ M)))
    return worst


def _gp4_residue(n=300):
    rank_dev_T = 0
    rank_dev_full = 0
    ward = 0.0
    for k in _bz_points(n, avoid_origin=True):
        O = Omega(k)
        if abs(np.sin(O)) < 1e-6:
            continue
        M = M6(O)
        lam, mu = np.exp(-1j * O), np.exp(1j * O)
        P = (M - mu * np.eye(6)) / (lam - mu)          # eigenprojector, e^{-iO}
        PT = PT6(k)
        RT = PT @ P @ PT                               # transverse residue
        rT = int(np.sum(np.linalg.svd(RT, compute_uv=False) > 1e-8))
        rF = int(np.sum(np.linalg.svd(P, compute_uv=False) > 1e-8))
        rank_dev_T = max(rank_dev_T, abs(rT - 2))
        rank_dev_full = max(rank_dev_full, abs(rF - 3))
        kh = k / np.linalg.norm(k)
        kvec6 = np.concatenate([kh, kh])
        ward = max(ward, np.max(np.abs(kvec6 @ RT)))
    return rank_dev_T, rank_dev_full, ward


def _gp5_eigenphases(n=500):
    worst = 0.0
    for k in _bz_points(n):
        O = Omega(k)
        ev = np.linalg.eigvals(M6(O))                  # real 6x6 (not chiral)
        worst = max(worst, np.max(np.abs(np.abs(np.angle(ev)) - O)))
    return worst


def _gp6_unitary_complete(n=500):
    unit = 0.0
    comp = 0.0
    for k in _bz_points(n):
        O = Omega(k)
        M = M6(O)
        unit = max(unit, np.max(np.abs(M @ M.T - np.eye(6))))
        if abs(np.sin(O)) < 1e-6:
            continue
        lam, mu = np.exp(-1j * O), np.exp(1j * O)
        Pp = (M - mu * np.eye(6)) / (lam - mu)
        Pm = (M - lam * np.eye(6)) / (mu - lam)
        comp = max(comp, np.max(np.abs(Pp + Pm - np.eye(6))))
    return unit, comp


def _gp7_doubler_scan(g=61):
    ax = np.linspace(-np.pi, np.pi, g)
    mn = np.inf
    zeros = set()
    for i in ax:
        for j in ax:
            for l in ax:
                O = Omega([i, j, l])
                if O < mn:
                    mn = O
                if O < 1e-6:
                    zeros.add((round(i, 6), round(j, 6), round(l, 6)))
    return mn, sorted(zeros)


def _gp8_independent_residue(n=300):
    worst = 0.0
    for k in _bz_points(n, avoid_origin=True):
        O = Omega(k)
        if abs(np.sin(O)) < 1e-6:
            continue
        M = M6(O)
        lam, mu = np.exp(-1j * O), np.exp(1j * O)
        Pcf = (M - mu * np.eye(6)) / (lam - mu)
        ev, V = np.linalg.eig(M)
        Vs = V[:, np.abs(ev - lam) < 1e-9]
        Peig = Vs @ np.linalg.pinv(Vs)
        worst = max(worst, np.max(np.abs(Pcf - Peig)))
    return worst


# ---------------------------------------------------------------- pytest
@pytest.mark.machine_precision
def test_gp1_pole_location_all_k():
    assert _gp1_pole_location() < 1e-12


@pytest.mark.exact
def test_gp2_massless_anchor():
    assert _gp2_massless_anchor() == 0.0


@pytest.mark.exact
def test_gp3_ward_commutator():
    assert _gp3_ward_commutator() == 0.0


@pytest.mark.machine_precision
def test_gp4_transverse_residue_and_ward():
    rT, rF, ward = _gp4_residue()
    assert rT == 0 and rF == 0
    assert ward < 1e-12


@pytest.mark.machine_precision
def test_gp5_eigenphases():
    assert _gp5_eigenphases() < 1e-12


@pytest.mark.machine_precision
def test_gp6_unitary_and_complete():
    unit, comp = _gp6_unitary_complete()
    assert unit < 1e-12 and comp < 1e-12


def test_gp7_single_gauge_pole_no_doubler():
    mn, zeros = _gp7_doubler_scan()
    assert mn == 0.0
    assert zeros == [(0.0, 0.0, 0.0)]


@pytest.mark.machine_precision
def test_gp8_independent_residue():
    assert _gp8_independent_residue() < 1e-12


# ---------------------------------------------------------------- dump
def main():
    gp1 = _gp1_pole_location()
    gp2 = _gp2_massless_anchor()
    gp3 = _gp3_ward_commutator()
    rT, rF, ward = _gp4_residue()
    gp5 = _gp5_eigenphases()
    unit, comp = _gp6_unitary_complete()
    mn, zeros = _gp7_doubler_scan()
    gp8 = _gp8_independent_residue()
    out = {
        "GP1_pole_location_max_det": gp1,
        "GP2_Omega_pair_0": gp2,
        "GP3_ward_commutator_max": gp3,
        "GP4_transverse_residue_rank_dev": rT,
        "GP4_full_residue_rank_dev": rF,
        "GP4_ward_k_dot_RT_max": ward,
        "GP5_eigenphase_err_max": gp5,
        "GP6_unitary_max": unit,
        "GP6_completeness_max": comp,
        "GP7_min_Omega_over_BZ": mn,
        "GP7_bz_zeros": zeros,
        "GP8_independent_residue_max_diff": gp8,
        "c_lat_slope": Omega([1e-5, 1e-5, 1e-5]) / (1e-5 * ROOT3),
    }
    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    with open(RESULT, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"\nwrote {RESULT}")


if __name__ == "__main__":
    main()
