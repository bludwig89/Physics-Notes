#!/bin/bash
# Quick-start for the Weyl CA live display.
# Run once to install dependencies, then launches the display.

cd "$(dirname "$0")"

# ── Find Python 3 ─────────────────────────────────────────────────
if command -v python3 &>/dev/null; then
    PY=python3
elif command -v python &>/dev/null; then
    PY=python
else
    echo "ERROR: Python not found. Install it from https://www.python.org"
    exit 1
fi

echo "Using: $($PY --version)"

# ── Install dependencies via python -m pip ─────────────────────────
echo "Installing dependencies..."
$PY -m pip install vispy PyQt6 numpy --quiet 2>/dev/null || \
$PY -m pip install vispy PyQt5 numpy --quiet 2>/dev/null || \
$PY -m pip install vispy PySide6 numpy --quiet

echo "Starting live display..."
$PY live_display.py
