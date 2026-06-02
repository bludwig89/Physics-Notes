"""F63 test runner — Einstein-Cartan spin-torsion magnitude estimate.
Exact-rational EC coefficient + real-arithmetic energy-density bookkeeping
evaluated at F62's actual packet densities (numpy safe; no chiral bilinear)."""
import json, os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
FORK = os.path.abspath(os.path.join(HERE, "..", "ca-simulation", "forks",
                                    "gr_fork_F63_spin_torsion_estimate.py"))
RESULTS = os.path.abspath(os.path.join(HERE, "..", "test-results",
                                       "F63_spin_torsion_estimate.json"))


def main():
    subprocess.run([sys.executable, FORK], check=True, cwd=os.path.dirname(FORK))
    with open(os.path.join(os.path.dirname(FORK), "f63_results.json")) as f:
        r = json.load(f)
    os.makedirs(os.path.dirname(RESULTS), exist_ok=True)
    with open(RESULTS, "w") as f:
        json.dump(r, f, indent=2)

    ok = True

    def chk(n, c, g):
        nonlocal ok
        ok = ok and c
        print(("PASS" if c else "FAIL"), n, "->", g)

    chk("EC four-fermion prefactor = 3/16 (exact)",
        r["coefficient"]["prefactor_3_16"] == "3/16",
        r["coefficient"]["prefactor_3_16"])
    chk("F61 cell a/ellP ~ 3.81 (g_*=16, d=3)",
        abs(r["cell"]["a_over_ellP"] - 3.809) < 0.01, r["cell"]["a_over_ellP"])
    chk("all 4 F62 configs evaluated (no silent skip)",
        r.get("n_f62_configs_evaluated", 0) == 4, r.get("n_f62_configs_evaluated", 0))
    chk("torsion negligible at F62 densities (0 < worst ratio < 1%)",
        0.0 < r["worst_f62_ratio"] < 1e-2, r["worst_f62_ratio"])
    chk("Cartan density > 1 quantum/cell (assumption only breaks super-densely)",
        r["cartan"]["f_star_cartan"] > 1.0, r["cartan"]["f_star_cartan"])

    print("\nALL PASS" if ok else "\nSOME FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
