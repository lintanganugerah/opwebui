<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-10 | Updated: 2026-04-10 -->

# scripts

## Purpose

Build and utility scripts for the ARSA project. These scripts handle offline preparation of the Pyodide Python runtime (used for browser-based code execution) and CycloneDX Software Bill of Materials (SBOM) generation from resolved dependency manifests. They run as part of the build pipeline or on-demand in CI.

## Key Files

| File | Description |
|------|-------------|
| `prepare-pyodide.js` | Node.js script that downloads Pyodide and a curated set of Python packages (numpy, pandas, matplotlib, scikit-learn, etc.), copies the runtime into `static/pyodide/`, and patches `pyodide-lock.json` with pure-Python wheels fetched from PyPI so micropip can install them offline |
| `generate-sbom.sh` | Bash script that produces a CycloneDX SBOM using Syft. Supports three modes: manifest-based generation (resolves Python deps via `uv pip compile`, reads `package-lock.json` for JS), Docker image scanning, and validation of an existing SBOM file |

## Subdirectories

This directory has no subdirectories.

## For AI Agents

### Working In This Directory

- Both scripts are standalone and do not import from other parts of the codebase.
- `prepare-pyodide.js` is an ES module script run with Node.js. It reads `package.json` for the Pyodide version and writes output to `static/pyodide/`.
- `generate-sbom.sh` requires external CLI tools: `syft` and `uv`. It reads `backend/requirements.txt` and `package-lock.json` and writes `sbom.cdx.json` to the project root.
- Do not add scripts here that belong in `backend/` (Python runtime) or `src/` (frontend build). This directory is for cross-cutting build utilities.

### Testing Requirements

- `prepare-pyodide.js`: manual verification. After running, check that `static/pyodide/pyodide-lock.json` exists and contains the expected packages.
- `generate-sbom.sh`: run with the `validate` argument (`./scripts/generate-sbom.sh validate`) to check the produced SBOM for format compliance and phantom local packages.

### Common Patterns

- Shell scripts use `set -euo pipefail` for strict error handling.
- The Node.js script uses top-level `await` (ESM) and `fs/promises` for async file operations.
- Both scripts are idempotent: re-running them safely overwrites previous output.

## Dependencies

### Internal

- `prepare-pyodide.js` reads `package.json` (for the Pyodide version) and writes to `static/pyodide/`.
- `generate-sbom.sh` reads `backend/requirements.txt` and `package-lock.json` from the project root.

### External

- `prepare-pyodide.js`: `pyodide` (npm package), `undici` (HTTP proxy support), `fs/promises` (Node built-in).
- `generate-sbom.sh`: `syft` (SBOM scanner), `uv` (Python dependency resolver), `python3` (for summary output).
