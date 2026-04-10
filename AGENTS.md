<!-- Generated: 2026-04-10 | Updated: 2026-04-10 -->

# Open WebUI

## Purpose

Open WebUI is an extensible, feature-rich, self-hosted AI platform designed to operate entirely offline. It supports LLM runners like Ollama and OpenAI-compatible APIs, with built-in inference for RAG. The project combines a Python/FastAPI backend with a SvelteKit frontend, shipped via Docker and installable through pip. Version 0.8.12.

## Key Files

| File | Description |
|------|-------------|
| `package.json` | Frontend dependencies and npm scripts (SvelteKit, Tailwind, Vitest, Cypress) |
| `pyproject.toml` | Backend Python dependencies (FastAPI, SQLAlchemy, LangChain, ChromaDB) and build config |
| `Dockerfile` | Multi-stage Docker build: Node.js frontend build, then Python backend image |
| `docker-compose.yaml` | Primary Docker Compose configuration for local deployment |
| `svelte.config.js` | SvelteKit config using adapter-static, outputs to `build/` directory |
| `vite.config.ts` | Vite build configuration for the frontend |
| `tsconfig.json` | TypeScript configuration for the frontend |
| `tailwind.config.js` | Tailwind CSS configuration |
| `postcss.config.js` | PostCSS configuration (used with Tailwind) |
| `.env.example` | Environment variable template (OLLAMA_BASE_URL, OPENAI_API_KEY, etc.) |
| `Makefile` | Docker Compose convenience targets (install, start, stop, update) |
| `i18next-parser.config.ts` | i18n extraction config for multilingual support |
| `cypress.config.ts` | Cypress end-to-end test configuration |
| `hatch_build.py` | Custom Hatch build hook for the Python package |
| `.pre-commit-config.yaml` | Pre-commit hooks configuration |
| `.eslintrc.cjs` | ESLint configuration for frontend linting |
| `.prettierrc` | Prettier code formatting config |
| `.npmrc` | npm configuration |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `backend/` | Python FastAPI backend: API routes, models, RAG retrieval, socket handling, migrations (see `backend/AGENTS.md`) |
| `src/` | SvelteKit frontend source: routes, components, stores, utilities, i18n (see `src/AGENTS.md`) |
| `cypress/` | Cypress end-to-end test specs, support files, and test data (see `cypress/AGENTS.md`) |
| `docs/` | Project documentation: contributing guide, security policy, Apache config (see `docs/AGENTS.md`) |
| `scripts/` | Build and utility scripts (Pyodide preparation, SBOM generation) |
| `static/` | Static assets served directly: themes, audio, Pyodide runtime, SQL.js, images, manifest |
| `test/` | Backend Python test files and test fixtures |
| `ref/` | Reference materials: branding inventory and summaries |
| `.github/` | GitHub Actions workflows, issue templates, Dependabot and FUNDING config |

## For AI Agents

### Working In This Directory

- This is a monorepo with two tech stacks: Python backend (`backend/`) and TypeScript/Svelte frontend (`src/`).
- The frontend builds to a `build/` directory via `npm run build`, which the backend then serves as static files.
- Always install both npm and Python dependencies before making changes.
- The backend entry point is `backend/open_webui/main.py`. The app factory is in `backend/open_webui/__init__.py`.
- Frontend dev server runs via `npm run dev` (Vite on port 5173). Backend dev runs via `backend/dev.sh`.
- Version is defined in `package.json` and read by `pyproject.toml` via Hatch. Do not update them independently.

### Testing Requirements

- Frontend unit tests: `npm run test:frontend` (Vitest)
- End-to-end tests: `npm run cy:open` or `cypress run` (Cypress)
- Backend tests: `pytest` in the `backend/` directory
- Lint all: `npm run lint` (runs eslint, svelte-check, and pylint)
- Type check frontend: `npm run check`

### Common Patterns

- Frontend uses Svelte 5 with runes (`$state`, `$derived`, `$effect`).
- Backend uses FastAPI routers under `backend/open_webui/routers/`.
- Database migrations managed by Alembic (`backend/open_webui/migrations/`).
- Socket.IO for real-time features (`backend/open_webui/socket/`).
- API client functions live in `src/lib/apis/`.
- Shared TypeScript types in `src/lib/types/`.
- i18n translations in `src/lib/i18n/`.

## Dependencies

### Internal

- `backend/` serves the frontend build from `src/`.
- `src/lib/apis/` calls backend REST endpoints.
- `src/routes/` maps to SvelteKit page routing.

### External

**Frontend (key):**
- Svelte 5 + SvelteKit (adapter-static)
- Tailwind CSS 4
- TipTap (rich text editor)
- CodeMirror (code editing)
- highlight.js + Shiki (syntax highlighting)
- Marked + Mermaid (markdown and diagram rendering)
- xterm.js (terminal emulation)
- Chart.js (data visualization)
- pdf.js (PDF rendering)
- socket.io-client (real-time communication)

**Backend (key):**
- FastAPI + Uvicorn (HTTP server)
- SQLAlchemy + Alembic (ORM and migrations)
- LangChain (RAG and LLM orchestration)
- ChromaDB (default vector database)
- OpenAI / Anthropic / Google GenAI SDKs
- Sentence-Transformers (embedding models)
- faster-whisper (speech-to-text)
- Redis (session storage)
- Authlib + python-jose + bcrypt (authentication)
- Hugging Face Transformers
