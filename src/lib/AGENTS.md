<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-10 | Updated: 2026-04-10 -->

# lib

## Purpose

Shared frontend library accessible via the `$lib` alias. Contains every piece of reusable client-side code: API client functions that talk to the backend, Svelte components organized by feature domain, global reactive stores, TypeScript type definitions, utility functions, i18n setup with locale files, web workers for off-thread computation, and the Pyodide kernel for browser-based Python execution. This directory is the backbone of the SvelteKit frontend.

## Key Files

| File | Description |
|------|-------------|
| `index.ts` | Placeholder file that marks this directory as the `$lib` import root. Currently contains only a comment. |
| `constants.ts` | Central runtime constants: API base URLs (`WEBUI_BASE_URL`, `OLLAMA_API_BASE_URL`, `OPENAI_API_BASE_URL`, etc.), app name, version references, supported file types and extensions, default model capabilities, and pasted text character limit. |
| `shortcuts.ts` | Keyboard shortcut registry. Defines the `Shortcut` enum and `shortcuts` map covering chat, global, input, and message actions with their key bindings, categories, and optional tooltips. |
| `dayjs.js` | Day.js entry point that eagerly imports 100+ locale files for full multilingual date formatting support across the app. |
| `emoji-groups.json` | Static JSON mapping of emoji groups used by the emoji picker component. |
| `emoji-shortcodes.json` | Static JSON mapping of emoji shortcodes to their Unicode characters. Consumed by `stores/index.ts` to build the reverse lookup `shortCodesToEmojis`. |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `apis/` | API client functions organized by backend domain (analytics, audio, auths, channels, chats, configs, evaluations, files, folders, functions, groups, images, knowledge, memories, models, notes, ollama, openai, prompts, retrieval, skills, streaming, tasks, terminal, tools, users, utils). The root `index.ts` handles models, pipelines, version, config, and tool server orchestration. |
| `components/` | Svelte components organized by feature: `admin/` (settings, users, analytics, evaluations, functions), `chat/` (main chat UI, messages, input, controls, model selector, artifacts, file nav, settings modal), `common/` (reusable UI primitives: modals, buttons, dropdowns, code editor, file items, emoji picker, etc.), `icons/` (176 individual SVG icon components), `layout/` (sidebar, navbar, search, archived chats), `workspace/` (models, knowledge, prompts, tools, skills editors), `channel/` (channel UI), `notes/` (notes UI), `playground/` (model playground). |
| `constants/` | Additional constant definitions. Currently contains `permissions.ts` with the default user permission structure covering workspace, sharing, chat, features, and settings. |
| `i18n/` | Internationalization setup using i18next. `index.ts` initializes i18next with browser language detection, lazy-loads locale JSON files from `locales/`, and exports the `i18n` Svelte store plus `changeLanguage` and `getLanguages` helpers. |
| `pyodide/` | Browser-based Python runtime. `pyodideKernel.ts` exposes a `PyodideKernel` class that communicates with a dedicated Web Worker (`pyodideKernel.worker.ts`) to execute Python code cells and stream stdout/stderr/results back to the main thread. |
| `stores/` | Global Svelte stores in a single `index.ts` file. Exports writable stores for config, user, models, chats, knowledge, tools, skills, functions, socket, theme, settings, banners, UI state (sidebar, search, settings panels), and typed interfaces for `Config`, `Settings`, `Model`, `SessionUser`, and related types. |
| `types/` | Shared TypeScript type definitions in `index.ts`. Currently exports `Banner` type and `TTS_RESPONSE_SPLIT` enum. |
| `utils/` | Utility functions in `index.ts` and sub-modules: markdown rendering helpers (`marked/`), code highlighting (`codeHighlight.ts`), CodeMirror setup (`codemirror.ts`), audio processing (`audio.ts`), cloud file picker integrations (`google-drive-picker.ts`, `onedrive-file-picker.ts`), Excel and PPTX conversion (`excelToTable.ts`, `pptxToHtml.ts`), text scaling (`text-scale.ts`), connection helpers (`connections.ts`), character utilities (`characters/`), and CSS transitions (`transitions/`). |
| `workers/` | Web Workers for off-main-thread computation. `kokoro.worker.ts` + `KokoroWorker.ts` handle browser-based TTS via the Kokoro model. `pyodide.worker.ts` runs Pyodide for the code interpreter feature. |

## For AI Agents

### Working In This Directory

- The `$lib` alias resolves here. Import as `$lib/apis`, `$lib/stores`, `$lib/types`, `$lib/constants`, `$lib/utils`, etc.
- This project uses **Svelte 5 with runes** (`$state`, `$derived`, `$effect`). Do not use legacy reactive patterns (`let` reactive declarations, `$:` statements, `$$props`).
- API clients in `apis/` follow a consistent pattern: async functions that call `fetch()` with Bearer token auth headers, then `.then()/.catch()` chains that extract JSON errors. New API clients should follow this exact pattern.
- Svelte stores are all defined in a single file (`stores/index.ts`). New global state should be added there as a `writable()` export.
- Components use Tailwind utility classes for styling. There are no CSS modules or scoped stylesheets.
- Icon components in `icons/` are individual `.svelte` files wrapping SVG markup. Add new icons by creating a new file following the existing pattern.
- The `utils/index.ts` file is large (1800+ lines). For new utility functions, check if a sub-module (`utils/marked/`, `utils/characters/`, etc.) is a better home before adding to the main file.
- i18n locale files live in `i18n/locales/<lang>/translation.json`. Use the `$t` function or `i18n` store for translatable strings.

### Testing Requirements

- Unit tests: `npm run test:frontend` (Vitest)
- Type checking: `npm run check` (svelte-check)
- Linting: `npm run lint` (eslint, svelte-check, pylint)

### Common Patterns

- **API clients**: Each domain in `apis/` has an `index.ts` exporting async functions. They accept `token` as the first argument and use `WEBUI_BASE_URL` from constants for the endpoint URL.
- **Stores**: Writable stores from `svelte/store`. Components subscribe via `$storeName` syntax in Svelte 5 or by importing and calling `.subscribe()`.
- **Components**: Svelte 5 component files (`.svelte`). Props use `$props()` rune. State uses `$state()` rune.
- **Workers**: New Web Workers should follow the pattern in `workers/KokoroWorker.ts` (wrapper class that instantiates the worker and manages a message queue).

## Dependencies

### Internal

- `src/routes/` consumes components, stores, and API clients from this directory.
- `apis/` calls backend REST endpoints at `/api/v1/...`, `/api/...`, `/ollama/...`, and `/openai/...`.
- `stores/index.ts` imports types from `types/`, constants from `constants.ts`, and API types from `apis/`.
- `utils/` depends on `constants.ts` for base URLs and `types/` for shared enums.

### External

- Svelte 5 + SvelteKit - UI framework and `$lib` alias resolution
- svelte/store - Writable stores for global state
- socket.io-client - Real-time WebSocket (store type reference)
- i18next + i18next-browser-languagedetector + i18next-resources-to-backend - Internationalization
- dayjs - Date formatting with full locale support
- marked - Markdown parsing and rendering
- highlight.js - Syntax highlighting
- pdf.js (pdfjs-dist) - PDF text extraction
- mammoth - DOCX text extraction
- mermaid - Diagram rendering
- vega + vega-lite - Data visualization
- uuid (v4) - Unique ID generation
- js-sha256 - SHA-256 hashing for Gravatar URLs
