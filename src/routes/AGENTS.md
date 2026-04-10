<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-10 | Updated: 2026-04-10 -->

# routes

## Purpose

SvelteKit file-based routing directory for ARSA. Every subdirectory maps to a URL path segment, and SvelteKit's convention of `+page.svelte`, `+layout.svelte`, and `+layout.js` files defines pages, nested layouts, and route options. The root layout (`+layout.svelte`) bootstraps the entire application: socket.io, i18n, theme handling, and all global Svelte stores. SSR is disabled at the root (`+layout.js` sets `export const ssr = false`), making this a client-side SPA.

## Key Files

| File | Description |
|------|-------------|
| `+layout.js` | Root route options. Disables SSR (`ssr = false`) and sets `trailingSlash = 'ignore'`. This makes the entire app a client-rendered SPA. |
| `+layout.svelte` | Root layout component (1082 lines). Initializes socket.io connection, i18n system, theme handling, all Svelte stores (config, user, settings, models, chats, tags, etc.), Pyodide worker, and navigation guards. The single entry point for all application state bootstrap. |
| `+error.svelte` | Global error boundary page. Displays the HTTP status code and error message in a minimal centered layout. |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `(app)/` | SvelteKit route group (no URL segment) wrapping the authenticated app shell. Contains its own `+layout.svelte` that loads models, tools, banners, and settings, then renders the sidebar and settings modal. All authenticated routes live here. |
| `auth/` | Authentication page at `/auth`. Handles sign-in, sign-up, LDAP login, and onboarding flows. A 605-line form component supporting multiple auth modes (credentials, LDAP, OAuth). |
| `error/` | Backend-unreachable error page at `/error`. Shown when the frontend cannot connect to the Python backend. Displays a "Backend Required" message with links to setup docs and Discord. |
| `s/` | Shared chat links at `/s/[id]`. Renders a shared conversation in read-only mode using `getChatByShareId`. Includes the option to clone the shared chat into the viewer's own chat list. |
| `watch/` | YouTube redirect at `/watch`. Extracts the `v` query parameter and redirects to `/?youtube=<videoId>` so YouTube links can be processed within the chat interface. |

### `(app)/` Subdirectories

These are the main authenticated routes, all nested under the `(app)/` route group:

| Directory | URL Path | Purpose |
|-----------|----------|---------|
| `(app)/admin/` | `/admin` | Admin panel. Default page redirects to `/admin/users`. Contains sub-routes for analytics, evaluations, functions, settings, and user management. |
| `(app)/c/[id]/` | `/c/:id` | Individual chat conversation view. Loads a specific chat by ID and renders the full chat interface. |
| `(app)/channels/[id]/` | `/channels/:id` | Individual channel view. Loads a specific channel by ID for real-time messaging. |
| `(app)/home/` | `/home` | Home dashboard page. Minimal layout with sidebar toggle and title. |
| `(app)/notes/` | `/notes` | Notes workspace. Supports creating, listing, and editing persistent notes. Accepts `title` and `content` query params to quick-create notes. Also has `/notes/new` and `/notes/[id]` sub-routes. |
| `(app)/playground/` | `/playground` | Model playground. Renders the playground chat component for testing models outside of saved conversations. Contains sub-routes for completions and image generation. |
| `(app)/workspace/` | `/workspace` | Workspace management. Contains sub-routes for functions, knowledge bases, custom models, prompts, skills, and tools. |

## For AI Agents

### Working In This Directory

- SvelteKit uses file-based routing. A `+page.svelte` file in any subdirectory becomes a routable page. A `+layout.svelte` wraps all child routes at that level and below.
- Route groups like `(app)/` use parentheses to create layout boundaries without affecting the URL path. The `(app)/` group shares a common sidebar and settings modal layout.
- Dynamic route segments use `[param]` brackets (e.g., `[id]`). Access the value via `$page.params.id` or `const { id } = $page.params` in `<script context="module">`.
- SSR is disabled globally in `+layout.js`. Do not add server-side logic (`+page.server.js`, `+page.ts` with `load`) in these routes. All data fetching happens client-side using `$lib/apis/` functions inside `onMount` or event handlers.
- The root `+layout.svelte` is the single largest file in the routes tree. It initializes nearly every global store and handles app-wide concerns. Changes here affect every page.
- Use `$app/stores` (`page`, `navigating`, `updated`) and `$app/navigation` (`goto`, `pushState`, `popState`) for routing logic.
- Import stores from `$lib/stores`, API functions from `$lib/apis/`, and components from `$lib/components/`.

### Testing Requirements

- Type checking: `npm run check` (svelte-check validates all `.svelte` files)
- E2E tests: Routes are tested via Cypress at `cypress/`. Look for test specs matching route paths.
- No standalone unit tests for route files. Route logic is tested through component tests and E2E suites.

### Common Patterns

- Every authenticated page lives under `(app)/`. The `(app)/+layout.svelte` loads models, tools, banners, and user settings on mount, then renders the sidebar and main content area.
- Pages typically call API functions in `onMount` to load data, then render `$lib/components/` components. Route files are thin wrappers; the heavy UI lives in the component library.
- The `+page.svelte` at the root of `(app)/` renders the main `Chat` component directly, making `/` the default chat interface.
- Error handling uses `toast.error()` from `svelte-sonner` for user-visible errors and `goto('/error')` for fatal failures.
- Navigation guards in root layout check auth state and redirect to `/auth` when no session exists.
- The `goto` function from `$app/navigation` is used for imperative redirects (e.g., admin default redirects to `/admin/users`).

## Dependencies

### Internal

- `$lib/stores` - Global reactive state consumed by every route (config, user, settings, models, chats, theme, socket, etc.)
- `$lib/apis/` - REST API client functions for fetching data from the backend
- `$lib/components/` - Shared UI components rendered within route pages
- `$lib/utils/` - Utility functions (i18n helpers, date formatting, text processing)
- `$lib/constants` - App-wide constants (WEBUI_API_BASE_URL, WEBUI_BASE_URL, etc.)
- `$lib/i18n` - Internationalization setup and translation functions
- `../app.css` and `../tailwind.css` - Global styles imported in root layout

### External

- SvelteKit - File-based routing, layouts, page options (`$app/stores`, `$app/navigation`)
- socket.io-client - Real-time connection initialized in root layout
- svelte-sonner - Toast notifications for error and success feedback
- dayjs - Date formatting in shared chat view and notes
- marked + dompurify - Markdown rendering and sanitization in auth page
- idb - IndexedDB wrapper used in `(app)/+layout.svelte` for local chat storage
- file-saver - File download helper used in `(app)/+layout.svelte`
