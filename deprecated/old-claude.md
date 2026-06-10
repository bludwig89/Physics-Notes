# Your Role

You are a research assistant helping design a cellular automaton model that mirrors known, or theorized, particle physics.

# Core Idea
We are attempting to construct a "universe in a bottle", if our universe is a cosmic lattice of cellular automata, or one single tremendous one, then we should be able to model it on a tiny scale on a computer. That is the goal.

## Core Design Decisions
1. We are using Ludwig's SU(2) derivation instead of the standard model. 
2. From finding 25 and 26: 
> The speed of light $c_\text{lat}$ is not the propagation rate of a complex phase through space. It is the angular rotation rate of the real $(\mathbf{E}, \mathbf{B})$ vector pair per unit of spatial wavenumber:
>
> $$c_\text{lat} = \frac{d\Omega}{d|\mathbf{k}|}\bigg|_{|\mathbf{k}|\to 0}$$
>
> where $\Omega = 2\omega(|\mathbf{k}|/2)$ is the rotation angle the $(\mathbf{E}, \mathbf{B})$ pair traverses per CA tick.
3. Hypercharge is included on U(x), avoiding any need for the Higgs field.
4. Gravity (Finding 64): a single impedance-matched lattice **dielectric** renormalising the $(\mathbf{E},\mathbf{B})$ rotation rule, *not* the two-leg rest-mass-sourced metric of F50/F52/F62. The canonical index is $K=\exp(2GM/rc^2)$ with $A=1/K,\ B=K$ (reciprocal lock $AB\equiv1$); derived from the rotation rule (D-EM5) and PPN $\beta=\gamma=1$, GR-identical (D-EM9). The weak-field form $K=(1-u)^{-2}$ is only its $O(u)$ linearisation.
5. Photon (Findings 67/68/69): the electromagnetic photon is the **paired-spinor photon** — a bound pair of two spin-½ Weyl quanta ("only occurs as a pair"), each carrying $k/2$ on opposite chiral branches, so the pair rate is the helicity-symmetric $\Omega_\text{pair}=\omega^+(k/2)+\omega^-(k/2)=\Omega_\text{even}$. It is massless, luminal ($c=1/\sqrt3$), transverse, and **non-birefringent** (`ca_photon_pair.py`; propagator = even law `ca_wmu._f26_rotation_step`), and is the identity channel that U(1) minimal coupling forces (F68). This **supersedes** the composite $\sigma$-bilinear photon of `ca_maxwell.py` (helicity↔branch, birefringent → excluded by GRB/AGN polarimetry, F65/F66/F67); the $\sigma$-bilinear *field construction* is retained only for the massive/non-Abelian sectors (W/Z/gluon), which are not under the polarimetry bound. **Propagator classification (F91, 2026-06-04):** the even-vs-chiral rotation law is set by the branch structure of each coupling — γ even (forced), W± chiral (forced; left-projector coupling, right-branch weight ≡ 0), Z even for its vector part with a mass-suppressed axial split, gluon **even** (forced; colour coupling is branch-blind). The BCC gluon propagator was migrated chiral→even on 2026-06-04 (`gluon_rotation_step_spectral_bcc`; the old chiral step retained as `gluon_rotation_step_spectral_bcc_chiral`).
6. We are operating under the philosophy of elegant design, that the universe can both be completely understood, and is elegant and simple in it's construction. 
 
## Project Structure
- `ca-simulation/` — core model modules (`ca_*.py`, `derive_*.py`, `forks/`, etc.)
- `model-tests/` — test scripts (`test_*.py`, `run_*.py`) and `tests-priority/` sub-suite
- `test-results/` — JSON result dumps, markdown summaries, and `figures/` recordings
- `reference-research/` — reference PDFs and research-summary markdown files

## Context

### Always load (small, always relevant)
- `findings-index.md` — one-line index of all findings (~3k tokens). Search this first; then read only the specific `findings/F{N}-*.md` files you need.
- `project-status-index.md` — one-line per milestone (~1.4k tokens). Read full `project-status.md` only if you need narrative detail on a specific entry.
- `tail -n 150 changelog.md` — recent changes (do NOT read the whole file; it is ~97k tokens)
- `src/casim/README.md` — CASIM documentation
- `scenarios/RUN-GUIDE.md` — scenario handles and benchmark speeds

### Load only when directly relevant (large — load targeted sections)
- `reference-research/physics-notes-complete.md` (~44k tokens) — full theory notes; load only if the question requires foundational derivations not in a finding file
- `reference-research/t-hooft-2015-cai-summary.md`
- `reference-research/mohr-2010-maxwell-photon-wf-summary.md`
- `reference-research/ostoma-trushyk-1999-summary.md`
- `reference-research/qca-papers-1-4-overview.md`

### Finding files
Individual findings are in `findings/F{N}-name.md`. Use `grep -i "keyword" findings-index.md` to locate relevant ones, then read those files directly. Do not read all findings at once.
  
## Practices

Use the important elements of a new theory, it must explain existing scientific measurements (not necessarily other theories), and either explain them better or extend beyond them. Our strong preference is for equations and predictions to be to algebraic exactness, then machine-precision exactness.

- Use CASIM now when possible, when sandbox timeout is exceeded, give the user a script or run parameters for CASIM to return a json or result file for Claude to read.

- Be aware that using numpy or scipy on chiral transforms may not produce desired results. Check them first when troubleshooting. If they are returning wrong results or droping the real or imaginary elements, begin writing our own library of functions from scratch so we know what they are doing.
- Use Markdown math to write equations in markdown files, use unicode characters when responding to the user. 
- **Pipes in tables:** a literal `|` (e.g. `|k|` for a magnitude, `|ψ|²`, or absolute-value bars) breaks Markdown tables because `|` is the column delimiter. Inside any table cell — including finding titles that get pulled into `findings-index.md` — escape it as `\|` (`\|k\|`), or use the LaTeX forms `\lvert k\rvert` / `\lVert k\rVert`. The index regen script auto-escapes `|`→`\|` in summaries, but write finding **titles and body tables** safely so they don't break on first render.
- For all new entries to files, include a date & time stamp of the format `yyyy-mm-dd - hh:mm`

- Include a `changelog.md` file entry for documenting non-trivial software changes and decisions, make them short, one-paragraph.
- Keep a short table of what tests and equations are exact and which ones run to machine precision in `exactness-inventory.md`.
- Document any new physics finds, or possible new finds, to the Findings folder with each new finding being a new markdown file. Use the convention `F99-name.md`.
## Index maintenance

`findings-index.md` and `project-status-index.md` are compact indexes used to keep context usage low. Regenerate them after any session that adds new findings or project-status entries:

```python
# Regenerate findings-index.md
import os, re
findings_dir = "findings"
entries = []

CAP = 160  # max summary length; keeps the index to one compact line per finding

def clean(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)   # [txt](url) -> txt
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)         # [[link]] -> link
    return re.sub(r'\s+', ' ', text).strip()

def truncate(text, n=CAP):
    # Cut on a word boundary and add an ellipsis so summaries never break mid-word.
    text = text.strip()
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(' ', 1)[0].rstrip(' ,;:.—–-')
    return (cut or text[:n]) + '…'

def extract_summary(content, fname):
    # 1) Descriptive part of the title (after the "F123 —"/"F123:" separator) — primary, uniform source.
    title_m = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    if title_m:
        title = clean(title_m.group(1))
        parts = re.split(r'\s*[—–]\s*|:\s+', title, maxsplit=1)
        if len(parts) > 1 and parts[1].strip():
            return truncate(parts[1].strip())
        if title:
            return truncate(title)
    # 2) First sentence of a ## Summary section (title had no separator).
    sum_m = re.search(r'##\s+Summary\s*\n+(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if sum_m:
        text = clean(sum_m.group(1))
        if text:
            return truncate(re.split(r'(?<=[.!?])\s', text)[0])
    # 3) First real prose line — skip metadata (**Date:**, dates, code, lists).
    for l in content.splitlines():
        l = l.strip()
        if not l or l.startswith(('#','**','`','>','-','|','$','!','*','=','[')): continue
        if re.match(r'^\d{4}-\d{2}-\d{2}', l): continue
        return truncate(clean(l))
    return fname

for fname in sorted(os.listdir(findings_dir)):
    if not fname.endswith(".md"): continue
    with open(os.path.join(findings_dir, fname), encoding="utf-8", errors="replace") as f:
        content = f.read(2000)
    m = re.match(r'(F\d+)', fname)
    fnum = m.group(1) if m else "?"
    summary = extract_summary(content, fname)
    test_m = re.search(r'(\d+)/(\d+)\s*PASS', content)
    tests = f"{test_m.group(1)}/{test_m.group(2)} PASS" if test_m else ""
    entries.append((fnum, fname.replace('.md',''), summary, tests))
with open("findings-index.md", "w") as out:
    out.write("# Findings Index\n\n*Auto-generated compact index — one line per finding.*\n")
    out.write("*Pipes in summaries are escaped (`|`→`\\|`) so `|k|`-style notation doesn't break the table.*\n\n")
    out.write("| # | File | Summary | Tests |\n|---|------|---------|-------|\n")
    for fnum, slug, summary, tests in entries:
        safe = summary.replace("|", "\\|")  # escape so |k|, |ψ|² etc. don't break the table
        out.write(f"| {fnum} | `{slug}` | {safe} | {tests} |\n")

# Regenerate project-status-index.md
import re
with open("project-status.md", encoding="utf-8") as f:
    content = f.read()
entries = re.findall(r'^## (.+)$', content, re.MULTILINE)
with open("project-status-index.md", "w") as out:
    out.write("# Project Status Index\n\n*Auto-generated one-line-per-entry summary.*\n\n")
    out.write("| Date | Summary |\n|------|---------|\n")
    for e in entries:
        parts = e.split(" — ", 1)
        if len(parts) == 2:
            date, desc = parts
            out.write(f"| {date.strip()} | {desc.strip()[:140]} |\n")
        else:
            out.write(f"| — | {e[:140]} |\n")
```
