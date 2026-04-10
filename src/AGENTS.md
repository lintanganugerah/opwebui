<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-10 | Updated: 2026-04-10 -->

# src

## Purpose

SvelteKit frontend source for Open WebUI. Contains all routes, components, API clients, stores, types, utilities, and global styles that make up the browser-facing application. The frontend builds to a static `build/` directory via `npm run build`, which the Python backend serves.

## Key Files

| File | Description |
|------|-------------|
| `app.html` | SvelteKit HTML shell. Handles theme detection (dark, light, oled-dark, her, system) before JS loads to avoid FOUC, sets up the splash screen with loading progress bar, and loads static assets (favicon, manifest, custom CSS, loader script). |
| `app.d.ts` | TypeScript ambient declarations for SvelteKit `App` namespace types (Error, Locals, PageData, Platform). |
| `app.css` | Global stylesheet. Declares custom fonts (Inter, Archivo, Mona Sans, InstrumentSerif, Vazirmatn), defines UI scale variables, and contains styles for TipTap/ProseMirror rich text editing, CodeMirror, highlight.js syntax colors, KaTeX math, Svelte Flow diagrams, scrollbar behavior, Tippy tooltips, shimmer animations, and markdown prose classes. |
| `tailwind.css` | Tailwind CSS v4 entry point. Imports the Tailwind framework, references the project's Tailwind config, defines the custom gray color palette (50 through 950 using oklch), and sets base layer styles for fonts, buttons, checkboxes, and placeholders. Includes a custom hover variant. |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `lib/` | Shared library code accessible via the `$lib` alias. Contains API clients, Svelte components, stores, types, utilities, i18n, web workers, and Pyodide runtime (see `lib/AGENTS.md`). |
| `routes/` | SvelteKit file-based routing. Each directory maps to a URL path. Contains page layouts, the main app shell, auth, error, shared links, and watch pages (see `routes/AGENTS.md`). |

## For AI Agents

### Working In This Directory

- This is a **SPA** (Single Page Application). SSR is disabled in `+layout.js` (`export const ssr = false`). All rendering happens client-side.
- The `$lib` alias resolves to `src/lib/`. Import shared code as `$lib/apis/...`, `$lib/stores`, `$lib/types`, etc.
- The project uses **Svelte 5 with runes** (`$state`, `$derived`, `$effect`). Do not use legacy Svelte 4 patterns (`let` reactive declarations, `$$props`, `$:` reactive statements).
- Global styles live in `app.css` and `tailwind.css`. Component-specific styles use Tailwind utility classes directly in templates.
- The root layout (`routes/+layout.svelte`) initializes socket.io, i18n, theme handling, and all Svelte stores. Most app state flows from here.
- Theme detection runs in `app.html` before JavaScript loads. Any theme logic that needs to avoid flash-of-unstyled-content belongs there.
- The frontend builds to `build/` via SvelteKit's `adapter-static`. The backend serves this directory as static files.

### Testing Requirements

- Unit tests: `npm run test:frontend` (Vitest)
- E2E tests: `npm run cy:open` or `cypress run` (Cypress)
- Type checking: `npm run check` (svelte-check)
- Linting: `npm run lint` (eslint, svelte-check, pylint)

### Common Patterns

- API client functions in `lib/apis/` call backend REST endpoints and return typed responses.
- Svelte stores in `lib/stores/index.ts` hold global state (config, user, settings, theme, socket, chats, models, etc.).
- Components follow a flat or shallow nested structure in `lib/components/`, organized by feature domain.
- i18n uses a custom setup in `lib/i18n/` backed by locale JSON files. Use the `$t` function or `i18n` store for translatable strings.
- Web workers handle heavy computation off the main thread: Kokoro TTS and Pyodide Python runtime.

## Dependencies

### Internal

- `backend/` serves the compiled `build/` output from this directory.
- `lib/apis/` calls backend REST endpoints at `/api/v1/...`.
- `static/` provides fonts, images, and other assets referenced from styles and templates.

### External

- Svelte 5 + SvelteKit (adapter-static) - UI framework and build system
- Tailwind CSS 4 - Utility-first CSS
- socket.io-client - Real-time WebSocket communication
- TipTap (ProseMirror) - Rich text editor
- CodeMirror - Code editing
- highlight.js + Shiki - Syntax highlighting
- Marked + Mermaid - Markdown and diagram rendering
- KaTeX - LaTeX math rendering
- dayjs - Date formatting with full locale support
- Svelte Flow - Node-based diagram editor
- xterm.js - Terminal emulation
- pdf.js - PDF rendering
- Chart.js - Data visualization
- Tippy.js - Tooltip library
- svelte-sonner - Toast notifications
