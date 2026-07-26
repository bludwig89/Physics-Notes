"""
F256 -- E1: 'derive lambda6=0.243' is structurally misposed; the dynamical
Landau route cannot give EXACT 3delta=Q, and lambda6 is derivative in both
pictures.

Verifies:
  L1  the convention-free target 3delta*=Q holds only to ~1.7e-5 (near-coincidence).
  L2  the lambda6 required for EXACT 3delta=Q is ~0.243, strictly BETWEEN the two
      available O(1) rationals (Fierz 2/9, rotor 1/4) and matching NEITHER
      (2/9 -> ~20% off in delta; 1/4 -> ~5% off).
  L3  B (Dirac sea, F95) and C (induced condensate coupling, F150) have
      independent O(1) origins -> the minimiser -B/2C has no mechanism to equal
      cos(2/3) exactly (finite sensitivity d(3delta)/dlambda6, no rational lock).
  L4  weight-as-phase (delta=2/9 primary) makes lambda6 an OUTPUT, not an input.

Real arithmetic; PDG masses; established F95/F118 |B|,C. No chiral transforms.
"""
import numpy as np

me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
m = np.array([mtau, mmu, me]) / mtau
s = np.sqrt(m)
ybar = s.mean()
Q = m.sum() / s.sum() ** 2
e = np.sqrt(3) * ybar          # E_g amplitude e = |p| = sqrt3 ybar ~ 0.728
B = -0.0569                    # |B| from the F95 sea closed form (F118 convention)


def _delta_of_lambda6(lam6):
    C = lam6 * e ** 6
    return np.arccos(np.clip(-B / (2 * C), -1, 1)) / 3


def test_L1_target_is_near_coincidence():
    c_dev = s / ybar - 1.0
    a = np.arange(3)
    Cc = np.sum(c_dev * np.cos(2 * np.pi * a / 3))
    Ss = np.sum(c_dev * np.sin(2 * np.pi * a / 3))
    d = (np.arctan2(-Ss, Cc)) % (2 * np.pi / 3)
    d = min(d, 2 * np.pi / 3 - d)
    resid = abs(3 * d - Q)
    assert 1e-6 < resid < 1e-4          # a ~1.7e-5 near-coincidence, not exact


def test_L2_required_lambda6_no_clean_rational():
    lam6_req = abs(B) / (2 * np.cos(Q) * e ** 6)
    assert abs(lam6_req - 0.243) < 3e-3          # ~0.243
    assert 2 / 9 < lam6_req < 0.25               # strictly between 2/9 and 1/4
    # the two clean rationals both MISS the angle
    d_29 = _delta_of_lambda6(2 / 9)
    d_14 = _delta_of_lambda6(0.25)
    assert abs(d_29 - 2 / 9) / (2 / 9) > 0.10    # 2/9 -> >10% off
    assert abs(d_14 - 2 / 9) / (2 / 9) > 0.02    # 1/4 -> >2% off


def test_L3_finite_sensitivity_no_lock():
    lam6_req = abs(B) / (2 * np.cos(Q) * e ** 6)
    h = 1e-6
    d3 = (_delta_of_lambda6(lam6_req + h) - _delta_of_lambda6(lam6_req - h)) / (2 * h) * 3
    assert d3 > 1.0    # finite, nonzero sensitivity: no structural lock at 3delta=Q


def test_L4_weight_as_phase_lambda6_is_output():
    # delta=2/9 primary -> C (hence lambda6) fixed as an OUTPUT
    lam6_out = abs(B) / (2 * np.cos(2 / 3) * e ** 6)
    assert abs(lam6_out - 0.243) < 3e-3


if __name__ == "__main__":
    for k, v in sorted(globals().items()):
        if k.startswith("test_"):
            v(); print("PASS", k)
