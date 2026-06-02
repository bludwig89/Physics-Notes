"""F61 test runner — Weyl heat-kernel eta and gravitating mode count g_*.
Exact rationals + a real-arithmetic lattice eigenphase-symmetry check (numpy safe)."""
import json, os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
FORK = os.path.abspath(os.path.join(HERE, "..", "ca-simulation", "forks",
                                    "gr_fork_F61_weyl_eta_gstar.py"))
RESULTS = os.path.abspath(os.path.join(HERE, "..", "test-results",
                                       "F61_weyl_eta_gstar.json"))

def main():
    subprocess.run([sys.executable, FORK], check=True, cwd=os.path.dirname(FORK))
    with open(os.path.join(os.path.dirname(FORK), "f61_results.json")) as f: r = json.load(f)
    os.makedirs(os.path.dirname(RESULTS), exist_ok=True)
    with open(RESULTS, "w") as f: json.dump(r, f, indent=2)
    ok = True
    def chk(n, c, g):
        nonlocal ok; ok = ok and c; print(("PASS" if c else "FAIL"), n, "->", g)
    chk("eta_Weyl = 1/12", r["heat_kernel"]["weyl"]["eta"] == "1/12", r["heat_kernel"]["weyl"]["eta"])
    chk("BCC eigenphases share |omega| (machine prec)",
        r["phase_space"]["eigenphase_abs_diff_max"] < 1e-12, r["phase_space"]["eigenphase_abs_diff_max"])
    chk("g_* (one gen, incl nuR) = 16", r["gstar"]["g_with_nuR_16"] == 16, r["gstar"]["g_with_nuR_16"])
    a16 = r["assembly"]["one_gen_nuR_16"]["a_over_ellP"]
    chk("a/ellP (g_*=16, d=3) ~ 3.81", abs(a16-3.809) < 0.01, a16)
    print("\nALL PASS" if ok else "\nSOME FAILED"); sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
