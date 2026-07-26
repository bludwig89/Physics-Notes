"""
F255 -- E1 follow-up: the F118/F234 solve fixes the E_g generator norm (R=1)
by Schur, but not the weight-identity (lambda6 stays circular).

Verifies:
  N1  the lepton deviation vector p = sqrt(m) - mean lies in the E_g plane
      (perpendicular to (1,1,1)) to machine precision.
  N2  the E_g invariant metric is isotropic (generators act orthogonally,
      D^T D = I) -> by Schur the E_g-plane angle is canonical: R=1 is FORCED,
      not posited (upgrades F253 POSIT-N part (a)).
  N3  the genuine geometric E_g-plane angle delta equals the Koide azimuth and
      equals 2/9 rad to <0.01% (both foldings agree).
  N4  the weight-identity is NOT independently fixed: cos3d*=-B/2C needs
      lambda6; F234 gets lambda6=0.243 by assuming 2/9 (circular); lambda6=1/4
      (rotor) gives delta ~5% off 2/9. So E1 does not close; residual = lambda6.

Real/exact arithmetic; no chiral transforms.
"""
import numpy as np

me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
s = np.sqrt(np.array([mtau, mmu, me]))
ybar = s.mean()
p = s - ybar
B = -0.0569  # derived cubic (F95)


def test_N1_deviation_in_Eg_plane():
    assert abs(p @ np.ones(3)) / np.linalg.norm(p) < 1e-12


def test_N2_Eg_metric_isotropic_schur():
    sites = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
    u = np.array([2*z*z-x*x-y*y for (x,y,z) in sites], float)
    w = np.array([x*x-y*y       for (x,y,z) in sites], float)
    u /= np.linalg.norm(u); w /= np.linalg.norm(w)
    gens = [lambda v:(v[2],v[0],v[1]),       # C3 about (1,1,1)
            lambda v:(-v[1],v[0],v[2]),      # C4 about z
            lambda v:(v[0],-v[1],-v[2])]     # C2 about x
    for f in gens:
        perm = [sites.index(f(v)) for v in sites]
        uP, wP = u[perm], w[perm]
        D = np.array([[uP@u, wP@u], [uP@w, wP@w]])
        assert np.max(np.abs(D.T @ D - np.eye(2))) < 1e-9  # orthogonal => isotropic


def test_N3_geometric_angle_is_2_9():
    u1 = np.array([2,-1,-1], float); u1 /= np.linalg.norm(u1)
    u2 = np.array([0, 1,-1], float); u2 -= (u2@u1)*u1; u2 /= np.linalg.norm(u2)
    d_geom = np.arctan2(p@u2, p@u1) % (2*np.pi/3)
    d_geom = min(d_geom, 2*np.pi/3 - d_geom)
    assert abs(d_geom - 2/9) / (2/9) < 1e-4


def test_N4_weight_identity_circular():
    # assuming 2/9 pins C (F234)
    C_req = abs(B) / (2*np.cos(3*(2/9)))
    assert abs(C_req - 0.0362) < 5e-4
    e6 = C_req / 0.243                     # e ~ 0.728 (F92 saturation)
    # lambda6 = 1/4 does NOT reproduce 2/9 (miss > 2%)
    d_quarter = np.arccos(-B / (2*0.25*e6)) / 3
    assert abs(d_quarter - 2/9)/(2/9) > 0.02


if __name__ == "__main__":
    for k, v in sorted(globals().items()):
        if k.startswith("test_"):
            v(); print("PASS", k)
