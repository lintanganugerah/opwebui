<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-10 | Updated: 2026-04-10 -->

# open_webui

## Purpose

The core Python package for ARSA's backend. Contains the FastAPI application factory, all API route handlers, database models, RAG retrieval pipeline, WebSocket layer, migration system, storage abstraction, and shared utilities. This is the package that gets installed via pip and runs inside Docker. The Typer CLI entry point lives in `__init__.py`, and the full FastAPI app wiring is in `main.py`.

## Key Files

| File | Description |
|------|-------------|
| `__init__.py` | Typer CLI entry point. Defines `serve` and `dev` commands, handles secret key generation and CUDA library path setup. 96 lines. |
| `main.py` | FastAPI application assembly. Imports and mounts all routers, configures middleware (CORS, session, compression, audit logging), serves static files, and attaches the Socket.IO app. ~2593 lines. |
| `config.py` | Central configuration hub. Loads environment variables into Pydantic settings models, defines database connection helpers, sets up OAuth providers, and exports feature flags. ~4030 lines. |
| `env.py` | Environment bootstrap. Resolves directory paths (`DATA_DIR`, `OPEN_WEBUI_DIR`, `BACKEND_DIR`), loads `.env`, configures logging, Redis, device type (CPU/CUDA/MPS), and exports global constants. ~944 lines. |
| `constants.py` | Enum constants for user-facing error messages (`ERROR_MESSAGES`), webhook messages (`WEBHOOK_MESSAGES`), and general notification strings (`MESSAGES`). 108 lines. |
| `tasks.py` | Async task management with Redis pub/sub. Tracks background tasks (generation, stop commands) across multiple Uvicorn workers. 210 lines. |
| `functions.py` | Plugin execution engine. Loads and runs user-defined Python functions, handles streaming responses and valve configuration for tools and filters. 340 lines. |
| `alembic.ini` | Alembic migration configuration. Points to `migrations/` directory and sets up logging for migration operations. 114 lines. |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `routers/` | FastAPI route modules. 28 router files covering auth, chats, ollama, openai, retrieval, images, audio, configs, users, models, tools, functions, knowledge, groups, and more. (see `routers/AGENTS.md`) |
| `models/` | SQLAlchemy/Pydantic model definitions and database CRUD functions. 22 model files for entities like auths, chats, files, knowledge, memories, models, users, and more. (see `models/AGENTS.md`) |
| `retrieval/` | RAG pipeline: document loaders, embedding/vector DB integrations, web search providers, reranker models, and retrieval utilities. ~1300 lines in `utils.py` alone. (see `retrieval/AGENTS.md`) |
| `socket/` | Socket.IO server for real-time features: chat streaming, model usage tracking, session management, and periodic cleanup tasks. 2 files, ~927 lines in `main.py`. (see `socket/AGENTS.md`) |
| `internal/` | Internal database layer. Contains SQLAlchemy base class, session factory (`get_db`), connection wrappers, and 18 legacy Peewee migration files. (see `internal/AGENTS.md`) |
| `migrations/` | Alembic migration environment. Holds `env.py`, migration templates, and `versions/` with 34 migration scripts covering schema evolution. (see `migrations/AGENTS.md`) |
| `utils/` | Shared utilities: auth helpers, OAuth, embeddings, rate limiting, Redis, PDF generation, code interpreter, MCP client, sanitization, webhooks, telemetry, ComfyUI integration, audit logging, and more. 27 utility files plus 4 subdirectories. (see `utils/AGENTS.md`) |
| `storage/` | File storage provider abstraction. Single file `provider.py` implementing local filesystem, S3, Google Cloud Storage, and Azure Blob Storage backends. (see `storage/AGENTS.md`) |
| `tools/` | Built-in tool definitions for the LLM tool-calling system. `builtin.py` provides web search, image generation, and memory tools that are available when native function calling is enabled. ~2326 lines. (see `tools/AGENTS.md`) |
| `test/` | Backend test suite. Contains test app fixtures and utility tests (Redis helpers). (see `test/AGENTS.md`) |
| `static/` | Static assets served by the backend: favicons, fonts, custom CSS, splash screens, swagger-ui, user import template, and the built frontend in `assets/`. (see `static/AGENTS.md`) |
| `data/` | Runtime data placeholder for Docker volumes. Contains a readme explaining its role for database and upload persistence. |

## For AI Agents

### Working In This Directory

- This is the `open_webui` Python package installed by pip. All imports use `from open_webui.<module> import ...`.
- The FastAPI `app` object is created in `main.py`. Every router is imported and mounted there.
- Configuration flows through `env.py` (raw env vars and paths) into `config.py` (Pydantic models with defaults). Add new settings to `config.py` using `BaseModel` subclasses.
- Database models follow a dual pattern: SQLAlchemy `Column` definitions for tables, Pydantic `BaseModel` for API schemas. CRUD operations are module-level functions in each model file.
- The `retrieval/` directory uses a factory pattern. Add vector DB providers in `retrieval/vector/dbs/` and register them in `retrieval/vector/factory.py`. Add web search providers in `retrieval/web/` and register them in `retrieval/web/main.py`.
- New API features follow this flow: create a model in `models/`, create a router in `routers/`, import the router in `main.py`.

### Testing Requirements

- Run tests with `pytest` from the `backend/` directory.
- Test files live in `test/` with test apps in `test/apps/` and utility tests in `test/util/`.
- Docker-based integration tests use `pytest-docker` for spinning up test databases.
- Lint with `pylint` (invoked via `npm run lint` from the project root).

### Common Patterns

- **Routers**: Each file creates an `APIRouter(prefix="/api/v1/...")` with dependency-injected database sessions (`get_db`) and auth checks (`get_current_user`, `get_admin_user`).
- **Models**: Dual schema pattern. SQLAlchemy table class + Pydantic request/response models + module-level CRUD functions.
- **Streaming**: Chat completions use `StreamingResponse` with async generators. Socket.IO emits events for real-time UI updates.
- **Task tracking**: Background tasks use Redis pub/sub in `tasks.py` so any worker can cancel a task started by another.
- **Storage**: `storage/provider.py` abstracts file operations behind a single interface. The backend is selected via the `STORAGE_PROVIDER` env var.
- **Configuration**: Pydantic models in `config.py` read env vars. The `PersistentConfig` class stores settings in the database for runtime changes without restarts.

## Dependencies

### Internal

- `routers/` imports from `models/`, `utils/`, `retrieval/`, and `socket/`.
- `models/` imports from `internal/` for database session management.
- `retrieval/` imports from `models/` and `utils/` for embeddings and file handling.
- `socket/` imports from `models/` and `utils/` for user lookup and event handling.
- Serves the built frontend from `../../src/` via static file mounting.

### External

- **Web framework**: FastAPI, Uvicorn, Starlette
- **Database**: SQLAlchemy, Alembic, Peewee (legacy migrations)
- **AI/ML**: LangChain, sentence-transformers, transformers, tiktoken, colbert-ai, faster-whisper
- **Vector DBs**: ChromaDB, PGVector, Milvus, Qdrant, Elasticsearch, OpenSearch, Pinecone, Oracle 23ai
- **LLM SDKs**: openai, anthropic, google-genai
- **Auth**: authlib, python-jose, bcrypt, argon2-cffi, PyJWT, ldap3
- **Storage**: boto3 (S3), google-cloud-storage, azure-storage-blob
- **Realtime**: python-socketio, Redis (starsessions)
- **Observability**: OpenTelemetry
- **Document processing**: pypdf, docx2txt, python-pptx, unstructured, rapidocr-onnxruntime
