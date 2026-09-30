"""
NB-045 (p.37): standard centered-difference discretization of the 2D wave equation.
NB-046 (pp.37-38): boxed explicit finite-difference update rule for the 2-component massless
Weyl CA:
    f(l,m,n,t+1) - f(l,m,n,t) = -c*(f(l,m,n+1,t)-f(l,m,n-1,t))
                                 -c*(g(l+1,m,n,t)-g(l-1,m,n,t))
                                 +i*c*(g(l,m+1,n,t)-g(l,m-1,n,t))
    g(l,m,n,t+1) - g(l,m,n,t) = -c*(f(l+1,m,n,t)-f(l-1,m,n,t))
                                 -i*c*(f(l,m+1,n,t)-f(l,m-1,n,t))
                                 +c*(g(l,m,n+1,t)-g(l,m,n-1,t))
    with c=1/2 in the notebook's own boxed version.
NB-047 (p.39): numerical stability exploration -- naive explicit scheme blows up without the 1/2
factors; empirical observation that it "stabilizes at ~0.43".

THIS SCRIPT REDOES THE NUMERICAL EXPERIMENT INDEPENDENTLY AND COLD: it implements exactly the
p.38 explicit-Euler update rule (not the split-step/FFT-propagator method a later, non-notebook
annotation in the transcription file used) on a 3D periodic grid, starting from the SAME kind of
generic (here: random) initial condition the notebook describes trying, and measures the norm
||psi||^2 over 200 steps for a sweep of c values, entirely with fresh code and no reference to
that annotation's stated conclusions.
"""
import numpy as np
import json, pathlib

rng = np.random.default_rng(20260922)  # seeded for determinism, per the task's reproducibility requirement

N = 24  # grid size per axis (periodic)
STEPS = 200


def run_explicit_euler(c, N=N, steps=STEPS, seed=20260922):
    rng_local = np.random.default_rng(seed)
    f = rng_local.normal(size=(N, N, N)) + 1j * rng_local.normal(size=(N, N, N))
    g = rng_local.normal(size=(N, N, N)) + 1j * rng_local.normal(size=(N, N, N))
    norm0 = np.sum(np.abs(f)**2 + np.abs(g)**2)

    norms = [1.0]
    for t in range(steps):
        # p.38 boxed update rule, exactly as transcribed (roll axis convention:
        # axis 0 = l (x-like, appears in the f,g cross terms), axis 1 = m (y-like, the i-terms),
        # axis 2 = n (z-like, the same-field terms) -- matches the notebook's (l,m,n) triple order.
        f_np1 = -c * (np.roll(f, -1, axis=2) - np.roll(f, 1, axis=2)) \
                - c * (np.roll(g, -1, axis=0) - np.roll(g, 1, axis=0)) \
                + 1j * c * (np.roll(g, -1, axis=1) - np.roll(g, 1, axis=1))
        g_np1 = -c * (np.roll(f, -1, axis=0) - np.roll(f, 1, axis=0)) \
                - 1j * c * (np.roll(f, -1, axis=1) - np.roll(f, 1, axis=1)) \
                + c * (np.roll(g, -1, axis=2) - np.roll(g, 1, axis=2))
        f_next = f + f_np1
        g_next = g + g_np1
        f, g = f_next, g_next
        norm_now = np.sum(np.abs(f)**2 + np.abs(g)**2)
        norms.append(norm_now / norm0)
        if not np.isfinite(norm_now) or norm_now > 1e12 * norm0:
            break
    return norms


c_values = [0.10, 0.20, 0.30, 0.35, 0.40, 0.43, 0.45, 0.50, 0.55, 0.60, 0.70]
sweep_results = {}
for c in c_values:
    norms = run_explicit_euler(c)
    final_ratio = norms[-1]
    max_ratio = max(norms)
    n_steps_survived = len(norms) - 1
    sweep_results[str(c)] = {
        "final_norm_ratio": float(final_ratio),
        "max_norm_ratio_over_run": float(max_ratio),
        "steps_completed_before_overflow_or_200": n_steps_survived,
        "grew_by_more_than_10x": bool(max_ratio > 10.0),
    }

result = {
    "build": "NB-045/NB-046/NB-047",
    "grid_size": N,
    "steps": STEPS,
    "seed": 20260922,
    "method": "explicit Euler, exactly the p.38 boxed update rule (forward difference in time, "
              "central difference in space), independent fresh implementation",
    "c_sweep": sweep_results,
    "notebook_own_claim": "notebook reports values grow from unity to ~11000 in ~10 steps "
                           "without the 1/2 factor (i.e. c=1 blows up fast, consistent with "
                           "2^10=1024 order-of-magnitude reasoning the author notes), and that "
                           "with the 1/2 in (c=0.5) it 'comes down to about 120 -- still not "
                           "ideal', with an empirical stabilization-like value around c~0.43.",
}
print(json.dumps(result, indent=2))

out = pathlib.Path(__file__).resolve().parents[3] / "test-results" / "notebook-recon" / "NB-045_046_047_spinor_ca_stability.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2))
print("wrote", out)
