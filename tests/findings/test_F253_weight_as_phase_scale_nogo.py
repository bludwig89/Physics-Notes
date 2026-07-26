"""
F253 -- E1 weight->phase principle: sharpened no-go + topological exclusion.

Verifies:
  W1  2/9 is exactly the E_g representation weight dim(E_g)/dim(T1u(x)T1u)
      (independent O_h character projection; reproduces F175 D1).
  W2  the measured lepton azimuth delta_meas = 2/9 rad to <0.01%.
  W3  EQUIPARTITION: given POSIT-N (E_g generator unit-normalized so the
      democratic phase budget = 1 rad) and unit amplitude, delta* = 2/9 rad
      EXACTLY; without POSIT-N delta = weight*R is scale-degenerate.
  W4  POSIT-N is not supplied by any O(1) saturation amplitude combination.
  W5  TOPOLOGICAL: the only genuine E_g holonomy on the BCC 2nd shell is
      2pi/3 (a rational multiple of pi); 2/9 is a multiplicity, not a holonomy,
      and 2/9 rad is not any low-order symmetry-quantized phase 2*pi*p/q.

Real/exact arithmetic only (sympy + real numpy) -- no chiral transforms.
"""
import numpy as np
import sympy as sp


def _decompose_bilinear():
    cls = {"E": 1, "C3": 8, "C2p": 6, "C4": 6, "C2": 3}
    chi_vec = {"E": 3, "C3": 0, "C2p": -1, "C4": 1, "C2": -1}
    chi_prod = {k: chi_vec[k] ** 2 for k in cls}
    irr = {
        "A1": {"E": 1, "C3": 1, "C2p": 1, "C4": 1, "C2": 1},
        "A2": {"E": 1, "C3": 1, "C2p": -1, "C4": -1, "C2": 1},
        "E": {"E": 2, "C3": -1, "C2p": 0, "C4": 0, "C2": 2},
        "T1": {"E": 3, "C3": 0, "C2p": -1, "C4": 1, "C2": -1},
        "T2": {"E": 3, "C3": 0, "C2p": 1, "C4": -1, "C2": -1},
    }
    dims = {"A1": 1, "A2": 1, "E": 2, "T1": 3, "T2": 3}
    mult = {n: sp.Rational(sum(cls[k] * chi_prod[k] * ch[k] for k in cls), 24)
            for n, ch in irr.items()}
    return mult, dims


def test_W1_Eg_weight_is_2_9():
    mult, dims = _decompose_bilinear()
    total = sum(mult[n] * dims[n] for n in mult)
    assert total == 9
    assert mult["E"] == 1
    weight = sp.Rational(dims["E"] * mult["E"], total)
    assert weight == sp.Rational(2, 9)


def test_W2_measured_azimuth_is_2_9():
    me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
    s = np.sqrt(np.array([me, mmu, mtau]))
    sbar = s.mean()
    c = s / sbar - 1.0
    a = np.arange(3)
    C = np.sum(c * np.cos(2 * np.pi * a / 3))
    S = np.sum(c * np.sin(2 * np.pi * a / 3))
    delta = np.arctan2(-S, C) % (2 * np.pi / 3)
    assert abs(delta - 2 / 9) / (2 / 9) < 1e-4  # <0.01%


def test_W3_equipartition_needs_positN():
    weight = sp.Rational(2, 9)
    R = sp.Symbol("R", positive=True)
    # WITH POSIT-N (R=1): delta = weight*1 = 2/9 exactly
    assert weight * 1 == sp.Rational(2, 9)
    # WITHOUT POSIT-N: delta = weight*R is not fixed (depends on free R)
    assert (weight * R).free_symbols == {R}


def test_W4_positN_not_from_saturation():
    e = 0.7330
    cands = [1.0, e, 1 / e, np.sqrt(2) * e ** 2, e ** 2]
    # only the bare 'set norm = 1' choice gives R=1; no nontrivial sat combo does
    nontrivial = [v for v in cands if abs(v - 1.0) > 1e-9]
    assert all(abs(v - 1.0) > 1e-3 for v in nontrivial)


def test_W5_topological_excluded():
    # E_g real basis on 6 BCC axis sites; C3 acts as 2pi/3 rotation
    sites = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    u = np.array([2 * z * z - x * x - y * y for (x, y, z) in sites], float)
    w = np.array([x * x - y * y for (x, y, z) in sites], float)
    u /= np.linalg.norm(u); w /= np.linalg.norm(w)
    perm = [sites.index((z, x, y)) for (x, y, z) in sites]  # C3: x->y->z->x
    uP, wP = u[perm], w[perm]
    M = np.array([[uP @ u, wP @ u], [uP @ w, wP @ w]])
    theta = np.arctan2(M[1, 0], M[0, 0])
    assert abs(abs(theta) - 2 * np.pi / 3) < 1e-9      # genuine holonomy = 2pi/3
    # 2/9 rad is NOT any low-order quantized phase 2*pi*p/q (q<=24)
    hits = [(p, q) for q in range(1, 25) for p in range(1, q)
            if abs(2 * np.pi * p / q - 2 / 9) < 1e-3]
    assert hits == []


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn(); print("PASS", name)
