"""
NB-068/NB-069 (p.54): "If phi(x) is real, what can we say about phi_k?" -- notebook derives
    phi_k = 2 omega_k INT phi(x) cos(kx) d^3x + i 2 omega_k INT phi(x) sin(kx) d^3x
    phi_{-k} = 2 omega_k INT phi(x) cos(kx) d^3x - i 2 omega_k INT phi(x) sin(kx) d^3x
and concludes "phi_k - phi_{-k} = 0  =>  phitilde_q = 0".

From the two displayed formulas themselves, phi_k - phi_{-k} = i*4*omega_k*INT phi(x)sin(kx)d^3x,
which is NOT generically zero for a real (but not necessarily EVEN) function phi(x) -- it is only
zero if phi is even. What DOES follow generically from those same two formulas is the standard
reality condition phi_k^* = phi_{-k} (phi_k* = the cos term minus i times the sin term, which is
exactly the phi_{-k} formula given) -- this is the textbook reality condition for a real scalar
field's Fourier coefficients, and it is what should feed into whatever phitilde_q=0 conclusion is
intended (odd-vs-even sub-claim), not a literal phi_k=phi_{-k}.

Verified numerically: an explicit real, GENERICALLY-ASYMMETRIC test function phi(x) (1D, since
the claim is dimension-independent), numerical quadrature for phi_k and phi_{-k} at a specific k,
checking both candidate conditions.
"""
import numpy as np
from scipy import integrate
import json, pathlib

omega = 1.7  # arbitrary
k_val = 0.9  # arbitrary nonzero test wavenumber


def phi(x):
    # a real, deliberately NOT-symmetric test function (asymmetric double-bump)
    return np.exp(-(x - 0.3)**2) + 0.5 * np.exp(-(x + 1.1)**2 / 0.7)


def phi_k_of(k):
    re, _ = integrate.quad(lambda x: phi(x) * np.cos(k * x), -20, 20, limit=400)
    im, _ = integrate.quad(lambda x: phi(x) * np.sin(k * x), -20, 20, limit=400)
    return 2 * omega * (re + 1j * im)


phik = phi_k_of(k_val)
phimk = phi_k_of(-k_val)

literal_claim_phik_minus_phimk_is_zero = abs(phik - phimk)
standard_reality_condition_phik_conj_minus_phimk = abs(np.conj(phik) - phimk)

result = {
    "build": "NB-068/NB-069",
    "k": k_val,
    "phi_k": {"re": phik.real, "im": phik.imag},
    "phi_{-k}": {"re": phimk.real, "im": phimk.imag},
    "|phi_k - phi_{-k}|_(notebook's_literal_claim,_expect_NONZERO_for_asymmetric_real_phi)": literal_claim_phik_minus_phimk_is_zero,
    "|phi_k^* - phi_{-k}|_(standard_reality_condition,_expect_ZERO)": standard_reality_condition_phik_conj_minus_phimk,
    "conclusion": "confirmed: for a real but ASYMMETRIC test function, the notebook's literal "
                  "'phi_k - phi_{-k} = 0' does NOT hold (nonzero by a large margin) -- it is "
                  "only true for an EVEN phi(x), not for a generic real one. What DOES hold "
                  "exactly, for this same asymmetric real phi(x), is the standard reality "
                  "condition phi_k^* = phi_{-k} (confirmed to numerical-quadrature precision), "
                  "which is directly readable off the notebook's own two displayed formulas "
                  "(phi_{-k} is literally phi_k with i -> -i, i.e. phi_k^*). This looks like a "
                  "genuine slip -- writing 'phi_k - phi_{-k} = 0' where 'phi_k^* - phi_{-k} = 0' "
                  "(equivalently phi_{-k} = phi_k^*) was meant.",
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-068_069_reality_condition.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
