<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-10 | Updated: 2026-04-10 -->

# test

## Purpose

Test fixtures and static resources used by integration and end-to-end tests. This directory holds binary and data files that tests mount or reference at runtime, keeping them separate from the Python test suites (which live under `backend/`).

## Key Files

| File | Description |
|------|-------------|
| `test_files/image_gen/sd-empty.pt` | Minimal PyTorch checkpoint used as a stub model for AUTOMATIC1111 Stable Diffusion WebUI integration tests |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `test_files/` | Root container for test fixture data |
| `test_files/image_gen/` | Image generation test fixtures |

## For AI Agents

### Working In This Directory

- This directory contains static test fixtures only. There are no Python test modules here.
- Backend Python tests live under `backend/open_webui/` and are run with `pytest` from the `backend/` directory.
- Frontend unit tests are colocated with source files under `src/` and run via `npm run test:frontend`.
- Cypress end-to-end tests live under `cypress/`.

### Testing Requirements

- Integration tests that need AUTOMATIC1111 use `docker-compose.a1111-test.yaml`, which mounts `test_files/image_gen/sd-empty.pt` as `/empty.pt` inside the Stable Diffusion container. This avoids downloading a real model during CI.
- To run the A1111 integration overlay: `docker compose -f docker-compose.yaml -f docker-compose.a1111-test.yaml up`.

### Common Patterns

- Fixture files should stay small. The `sd-empty.pt` stub is intentionally minimal so tests start quickly without GPU or large downloads.
- When adding new integration test fixtures, create a subdirectory under `test_files/` named after the feature area (e.g., `audio/`, `rag/`).

## Dependencies

### Internal

- `docker-compose.a1111-test.yaml` mounts `test_files/image_gen/sd-empty.pt` for image generation integration testing.
- `pyproject.toml` declares `pytest`, `pytest-docker`, and `pytest-asyncio` as test dependencies.

### External

- PyTorch (`.pt` file format for the Stable Diffusion stub checkpoint)
