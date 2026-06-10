# /test-priority — Run the priority test suite

Run all tests in `model-tests/tests-priority/` and save results.

## Steps

1. Get the current timestamp: `date "+%Y-%m-%d-%H%M"` → use as `{ts}`.

2. Run the suite from the project root:
   ```
   python -m pytest model-tests/tests-priority/ -v --tb=short 2>&1 | tee test-results/priority-run-{ts}.txt
   ```
   If pytest is unavailable, run each file individually with `python model-tests/tests-priority/test_*.py`.

3. Report a summary table:
   | Test file | PASS/FAIL | Notes |
   |-----------|-----------|-------|

4. If any test fails:
   - Show the traceback
   - Check whether the failure is in a module that was recently edited (check `changelog.md`)
   - Suggest the most likely fix

5. If all pass, offer to run the full `model-tests/` suite or a specific CASIM scenario.
