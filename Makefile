# casim — developer entry points.
#
# Roadmap P0.5. `make gate` is the fast correctness barrier that must be green
# before anything is committed; everything slower lives behind `make battery`.
#
# If you never host this repo on GitHub, `make gate` IS the gate — the Actions
# workflow in .github/workflows/gate.yml runs exactly the same script.

PY ?= python3
export PYTHONPATH := src

.DEFAULT_GOAL := gate
.PHONY: gate constants supersessions stamp battery indexes inventory \
        install backend manifest health numerics constants-report drift clean help \
        graph deadcode migration-manifest c0 migrate registry registry-gen \
        indexes-check

## install: editable install with the fast FFT backend and pytest
install:
	@$(PY) -m pip install -e '.[fast,dev]'
	@$(PY) -m casim.cli backend

## backend: show (and with BENCH=1, benchmark) the active FFT backend
backend:
	@$(PY) -m casim.cli backend $(if $(BENCH),--bench,)

## gate: the fast barrier — provenance + package suite + scenario smoke (<2 min)
gate:
	@$(PY) tools/run_gate.py

## constants: C2/D7 — assert no unregistered constant literal exists
constants:
	@$(PY) tests/casim/test_constants_consistency.py

## constants-report: list every rogue literal the C2.4 sweep can see
constants-report:
	@$(PY) tools/audit_constants.py --list

## supersessions: check docs/theory/supersessions.yaml is true and banners current
supersessions:
	@$(PY) tests/casim/test_supersession_ledger.py

## stamp: (re)write supersession banners from the ledger — run after editing it
stamp:
	@$(PY) tools/apply_supersession_banners.py

## manifest: rebuild test-results/manifest.json + the exactness inventory
manifest:
	@$(PY) -m casim.cli index --only results,exactness

## health: test-suite health report (unfalsifiable / import-time / debt counts)
health:
	@$(PY) tools/audit_tests.py

## registry: C7/D9 — test-registry coverage and validity (LIST=1 names the debt)
registry:
	@$(PY) tools/check_test_registry.py $(if $(LIST),--verbose,)

## registry-gen: rebuild tests/registry/*.yaml (PROMOTE=1 arms detected baselines)
registry-gen:
	@$(PY) tools/gen_test_registry.py $(if $(PROMOTE),--promote,)

## numerics: D8 report — modules still importing numpy/scipy/ca_fft directly
numerics:
	@$(PY) tools/audit_numerics.py $(if $(LIST),--list,)
	@$(PY) -m casim.cli backend 2>/dev/null || true

## drift: numeric drift in result artifacts vs git HEAD, after re-running physics
drift:
	@$(PY) tools/check_result_drift.py

## c0: rebuild the whole migration-readiness layer (graph -> dead code -> manifest)
c0: graph deadcode migration-manifest
	@$(PY) tools/check_deprecated.py

## graph: rebuild docs/design/module-graph.json (imports, reachability, sizing)
graph:
	@$(PY) tools/gen_module_graph.py

## deadcode: regenerate the dead/superseded PROPOSAL (never applied)
deadcode:
	@$(PY) tools/find_dead_code.py

## migration-manifest: rebuild the 171-record migration manifest
migration-manifest:
	@$(PY) tools/gen_migration_manifest.py

## migrate: move one module into casim.engine, e.g. `make migrate ID=ca_bcc.py`
migrate:
	@test -n "$(ID)" || (echo "usage: make migrate ID=ca_bcc.py [DRY=1]"; exit 1)
	@$(PY) tools/migrate_module.py --id $(ID) $(if $(DRY),--dry-run,)

## battery: the full scaled suite. Hours, not minutes. Not part of the gate.
battery:
	@$(PY) -m casim.cli test --scale smoke

## indexes: regenerate every generated index from the registries (C8)
indexes:
	@$(PY) -m casim.cli index

## indexes-check: fail if any generated index is stale (what `make gate` runs)
indexes-check:
	@$(PY) -m casim.cli index --check

## inventory: regenerate the casim-scoped exactness inventory
inventory:
	@$(PY) -m casim.cli inventory

clean:
	@find . -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache

help:
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/^## /  /'
