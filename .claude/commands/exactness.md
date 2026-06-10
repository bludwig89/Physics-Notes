# /exactness — Add a row to docs/status/exactness-inventory.md

Add one or more results to the exactness inventory table.

## Steps

1. Get the current date: `date "+%Y-%m-%d - %H:%M"`.

2. Ask the user (if not already in $ARGUMENTS) for each result:
   - **#** — next row number (read the table to find the current max)
   - **Construct** — short name (e.g. "Goldstone mass $m_\pi=0$")
   - **Predicted form** — the algebraic expression or identity
   - **Measured residual** — numerical value (e.g. `2.3×10⁻¹⁴`)
   - **Tier** — one of: `Exact algebraic`, `Machine precision`, `Quantitative`
   - **Source** — finding number and/or test file (e.g. `F77 / test_F77_njl.py`)

3. Append the row(s) to the correct tier section in `docs/status/exactness-inventory.md`:
   ```
   | {#} | {Construct} | {Predicted form} | {Measured residual} | {Source} |
   ```
   Update the "Last updated" line at the top of the file with the current timestamp and a one-line description of what was added.

4. Confirm the rows were added and show the updated lines.
