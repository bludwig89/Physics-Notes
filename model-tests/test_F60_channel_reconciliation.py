"""F60 test runner — tree-vs-loop reconciliation of the two induced-G channels.
Real arithmetic only (linear/arccos dispersions) -> numpy safe per CLAUDE.md."""
import json, os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
FORK = os.path.abspath(os.path.join(HERE, "..", "ca-simulation", "forks",
                                    "gr_fork_F60_channel_reconciliation.py"))
RESULTS = os.path.abspath(os.path.join(HERE, "..", "test-results",
                                       "F60_channel_reconciliation.json"))

def main():
    subprocess.run([sys.executable, FORK], check=True, cwd=os.path.dirname(FORK))
    with open(os.path.join(os.path.dirname(FORK), "f60_results.json")) as f: r = json.load(f)
    os.makedirs(os.path.dirname(RESULTS), exist_ok=True)
    with open(RESULTS, "w") as f: json.dump(r, f, indent=2)
    ok = True
    def chk(n, c, g):
        nonlocal ok; ok = ok and c; print(("PASS" if c else "FAIL"), n, "->", g)
    chk("bare stiffness = c_lat^2", abs(r["A_bare"]["p_S_vs_clat"]-2.0) < 1e-3, r["A_bare"]["p_S_vs_clat"])
    chk("S/c_lat^2 lock exact", r["A_bare"]["S_eq_clat2_spread"] < 1e-12, r["A_bare"]["S_eq_clat2_spread"])
    chk("induced stiffness = 1/c_lat", abs(r["B_induced"]["p_B_vs_clat"]+1.0) < 1e-3, r["B_induced"]["p_B_vs_clat"])
    chk("gap = c_lat^-3 (tree-vs-loop)", abs(r["C_gap"]["p_ratio_vs_clat"]+3.0) < 1e-3, r["C_gap"]["p_ratio_vs_clat"])
    print("\nALL PASS" if ok else "\nSOME FAILED"); sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
