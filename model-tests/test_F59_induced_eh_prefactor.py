"""F59 test runner — induced-EH prefactor + Finding-10 selection.
Runs the self-contained fork module and checks the load-bearing results.
Real arithmetic only (arccos dispersion) — numpy safe per CLAUDE.md.
"""
import json, os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
FORK = os.path.abspath(os.path.join(HERE, "..", "ca-simulation", "forks",
                                    "gr_fork_F59_induced_eh_prefactor.py"))
RESULTS = os.path.abspath(os.path.join(HERE, "..", "test-results",
                                       "F59_induced_eh_prefactor.json"))

def main():
    subprocess.run([sys.executable, FORK], check=True, cwd=os.path.dirname(FORK))
    src = os.path.join(os.path.dirname(FORK), "f59_results.json")
    with open(src) as f: r = json.load(f)
    os.makedirs(os.path.dirname(RESULTS), exist_ok=True)
    with open(RESULTS, "w") as f: json.dump(r, f, indent=2)

    ok = True
    def chk(name, cond, got):
        nonlocal ok; ok = ok and cond
        print(("PASS" if cond else "FAIL"), name, "->", got)

    chk("calibration Pi(0)~0.4466", abs(r["Pi0_fullBZ"]-0.4466) < 2e-3, r["Pi0_fullBZ"])
    chk("Newton sector ~ Lambda^2", abs(r["sectors"]["p_invw"]-2.0) < 0.15, r["sectors"]["p_invw"])
    chk("CC sector ~ Lambda^4",     abs(r["sectors"]["p_w"]-4.0) < 0.15, r["sectors"]["p_w"])
    Ic = [v["I_times_c"] for v in r["sqrt_d"].values()]
    chk("1/G ~ 1/c_lat = sqrt(d) (I*c const)", max(Ic)-min(Ic) < 1e-6, Ic)
    chk("naive stress-bubble UV-dominated (>>2)", r["naive_scaling_exponent"] > 4.0, r["naive_scaling_exponent"])
    A = r["assembly"]
    chk("selection a ~ d^1/4 ell_P", abs(A["a_over_ellP"]-1.347) < 0.02, A["a_over_ellP"])
    print("\nALL PASS" if ok else "\nSOME FAILED")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
