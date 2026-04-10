<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-10 | Updated: 2026-04-10 -->

# Backend

## Purpose

The Python/FastAPI backend for ARSA. It exposes a REST API and WebSocket layer that powers chat interactions, RAG retrieval, user authentication, model management, file storage, image generation, audio processing, and admin configuration. The application is served by Uvicorn and can run as a standalone pip package or inside a Docker container. The main package lives at `open_webui/`, with the FastAPI app factory in `__init__.py` and the route wiring in `main.py`.

## Key Files

| File | Description |
|------|-------------|
| `open_webui/__init__.py` | CLI entry point via Typer. Handles `arsa serve` and `arsa dev` commands, secret key generation, and CUDA setup. |
| `open_webui/main.py` | FastAPI application setup. Mounts routers, middleware (CORS, session, compression, audit logging), static files, and the Socket.IO app. ~2600 lines. |
| `open_webui/config.py` | Central configuration: environment variable loading, Pydantic settings models, database connection helpers, OAuth provider setup, feature flags. ~4000 lines. |
| `open_webui/env.py` | Environment bootstrap. Resolves directory paths, loads `.env`, configures logging, Redis, device type (CPU/CUDA), and exports global constants like `DATA_DIR`, `VERSION`. |
| `open_webui/constants.py` | Enum constants for error messages, webhook messages, and user-facing strings. |
| `open_webui/tasks.py` | Async task management with Redis pub/sub. Tracks background tasks (generation, stop commands) across workers. |
| `open_webui/functions.py` | Function (plugin) execution engine. Loads and runs user-defined Python functions, handles streaming responses, valve configuration. |
| `open_webui/alembic.ini` | Alembic migration configuration pointing to the SQLAlchemy database URL. |
| `requirements.txt` | Full Python dependency list (FastAPI, SQLAlchemy, LangChain, ChromaDB, OpenAI/Anthropic/Google SDKs, and ~100 other packages). |
| `requirements-min.txt` | Minimal dependency subset for lightweight Docker images. |
| `dev.sh` | Development launcher. Sets CORS origins for the Vite dev server and runs uvicorn with `--reload`. |
| `start.sh` | Production entry point for Docker. Handles secret key generation, Ollama/CUDA setup, Playwright installation, HuggingFace Spaces config, and multi-worker uvicorn launch. |
| `start_windows.bat` | Windows equivalent of `start.sh` for non-WSL setups. |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `open_webui/routers/` | FastAPI route modules. Each file is a router (auths, chats, ollama, openai, retrieval, images, audio, configs, users, etc.). 28 routers total. |
| `open_webui/models/` | SQLAlchemy/Pydantic model definitions and database access functions for each entity (auths, chats, files, knowledge, memories, models, users, etc.). 22 model files. |
| `open_webui/retrieval/` | RAG pipeline: document loaders, embedding/vector DB integrations, web search providers, and reranker models. |
| `open_webui/retrieval/loaders/` | Document content extractors (main loader, YouTube, Mistral OCR, Tika/external, Tavily, Marker, MinerU). |
| `open_webui/retrieval/vector/` | Vector database abstraction layer with factory pattern. Supports ChromaDB, PGVector, Milvus, Qdrant, Weaviate, Elasticsearch, OpenSearch, Pinecone, S3Vector, Oracle 23ai, and more. |
| `open_webui/retrieval/web/` | Web search provider integrations (SearXNG, Google PSE, Brave, DuckDuckGo, Kagi, Tavily, Perplexity, Exa, Bing, Jina, and ~20 others). |
| `open_webui/retrieval/models/` | Reranker model implementations (ColBERT, external rerankers). |
| `open_webui/socket/` | Socket.IO server for real-time features: chat streaming, model usage tracking, session management, periodic cleanup tasks. |
| `open_webui/internal/` | Internal database layer: SQLAlchemy base, session factory (`get_db`), and legacy Peewee migrations (18 migration files). |
| `open_webui/migrations/` | Alembic migration environment. Holds `env.py`, migration templates, and `versions/` directory for migration scripts. |
| `open_webui/utils/` | Shared utilities: auth, OAuth, embeddings, rate limiting, Redis helpers, PDF generation, code interpreter, MCP client, sanitization, webhooks, telemetry, image generation (ComfyUI), audit logging, and more. |
| `open_webui/utils/access_control/` | Permission checking utilities for file-level access control. |
| `open_webui/utils/images/` | ComfyUI integration for local image generation. |
| `open_webui/utils/mcp/` | Model Context Protocol client for tool/function integration. |
| `open_webui/utils/telemetry/` | OpenTelemetry setup: instrumentors, metrics, logs, and traces for production observability. |
| `open_webui/storage/` | File storage provider abstraction (local filesystem, S3, GCS, Azure Blob). |
| `open_webui/tools/` | Built-in tool definitions for the LLM tool-calling system. |
| `open_webui/test/` | Backend test suite: test apps and utility tests. |
| `open_webui/static/` | Static assets served by the backend: favicons, fonts, custom CSS, swagger-ui, and the built frontend (`assets/`). |
| `open_webui/data/` | Runtime data placeholder (database, uploads). Contains a readme noting its purpose for Docker volumes. |
| `data/` | Docker volume mount point for persistent storage (database, uploads, documents). Contains a readme describing its role. |

## For AI Agents

### Working In This Directory

- The backend runs as the `open_webui` Python package. Install dependencies from `requirements.txt` before making changes.
- Entry point: `open_webui/__init__.py` defines the Typer CLI. The FastAPI `app` object is created in `open_webui/main.py`.
- For local development, use `dev.sh`. It sets CORS for the Vite frontend (`localhost:5173`) and enables hot reload.
- All routers are registered in `main.py`. When adding a new feature, create a router file in `routers/` and import it in `main.py`.
- Database models live in `models/`. Each model file defines both the SQLAlchemy table and Pydantic schemas, plus CRUD helper functions.
- Configuration is centralized in `config.py` and `env.py`. Prefer adding new settings to `config.py` using Pydantic `BaseModel` classes.
- The `retrieval/` directory uses a factory pattern for both vector databases (`retrieval/vector/factory.py`) and web search (`retrieval/web/main.py`). Add new providers by creating a module and registering it in the factory.

### Testing Requirements

- Run tests with `pytest` from the `backend/` directory.
- Test files live in `open_webui/test/`.
- Docker-based integration tests use `pytest-docker` for spinning up test databases.
- Lint with `pylint` (invoked via `npm run lint` from the project root).

### Common Patterns

- **Routers**: Each router file follows the pattern `APIRouter(prefix="/api/v1/...")` with dependency-injected database sessions (`get_db`) and auth checks (`get_current_user`, `get_admin_user`).
- **Models**: Dual pattern with SQLAlchemy `Column` definitions for DB tables and Pydantic `BaseModel` for request/response schemas. CRUD operations are module-level functions.
- **Streaming**: Chat completions use `StreamingResponse` with async generators. The socket layer (`socket/main.py`) emits events for real-time updates.
- **Task management**: Background tasks are tracked via Redis pub/sub in `tasks.py`, enabling cross-worker cancellation.
- **Plugin system**: User-defined Python functions are loaded dynamically via `utils/plugin.py` with sandboxed execution using `RestrictedPython`.
- **Storage abstraction**: `storage/provider.py` provides a unified interface for local, S3, GCS, and Azure Blob storage backends.

## Dependencies

### Internal

- Serves the built frontend from `../src/` (static files mounted from `FRONTEND_BUILD_DIR`).
- Frontend API client in `../src/lib/apis/` calls these backend endpoints.
- Version is defined in `../package.json` and read via Hatch in `../pyproject.toml`.

### External

- **Web framework**: FastAPI + Uvicorn + Starlette
- **Database**: SQLAlchemy + Alembic (migrations), Peewee (legacy migrations)
- **AI/ML**: LangChain, sentence-transformers, transformers, tiktoken, colbert-ai, faster-whisper
- **Vector DBs**: ChromaDB, PGVector, Milvus, Qdrant, Weaviate, Elasticsearch, OpenSearch, Pinecone, Oracle 23ai
- **LLM SDKs**: openai, anthropic, google-genai
- **Auth**: authlib, python-jose, bcrypt, argon2-cffi, PyJWT, LDAP (ldap3)
- **Storage**: boto3 (S3), google-cloud-storage, azure-storage-blob
- **Realtime**: python-socketio, Redis (starsessions)
- **Observability**: OpenTelemetry (traces, metrics, logs)
- **Document processing**: pypdf, docx2txt, python-pptx, unstructured, rapidocr-onnxruntime
- **Web search**: ddgs (DuckDuckGo), firecrawl, playwright, and ~25 other provider SDKs
- **Cloud integrations**: azure-ai-documentintelligence, google-api-python-client
