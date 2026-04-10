<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-10 | Updated: 2026-04-10 -->

# static

## Purpose

Static assets served directly to the browser without processing. Contains fonts, emoji SVGs, audio clips, WebAssembly runtimes (Pyodide and sql.js), PWA icons and manifests, browser integration configs, and custom CSS themes. These files are shipped as-is alongside the SvelteKit build output.

## Key Files

| File | Description |
|------|-------------|
| `manifest.json` | Empty JSON placeholder (SvelteKit app manifest) |
| `opensearch.xml` | OpenSearch description for browser search engine integration |
| `robots.txt` | Disallows all crawler access (`User-agent: *`, `Disallow: /`) |
| `favicon.png` | Default site favicon |
| `image-placeholder.png` | Placeholder image for missing or loading images |
| `user.png` | Default user avatar |
| `marker-icon-2x.png` | Retina Leaflet map marker icon |
| `marker-icon.png` | Standard Leaflet map marker icon |
| `marker-shadow.png` | Leaflet map marker shadow |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `assets/` | Fonts, emoji SVGs, and sample background images (see `assets/AGENTS.md`) |
| `audio/` | UI sound effects: greeting and notification MP3 clips |
| `pyodide/` | Pyodide WebAssembly runtime lock file for in-browser Python execution |
| `sql.js/` | sql.js WebAssembly binary (`sql-wasm.wasm`) for client-side SQLite |
| `static/` | PWA assets: favicons, splash screens, web manifest, logo, custom CSS override, and user import CSV template |
| `themes/` | Custom CSS theme files (Rosé Pine and Rosé Pine Dawn) |

## For AI Agents

### Working In This Directory

- This directory is for static, pre-built assets only. Do not add source code here.
- The backend serves files from this directory via FastAPI's static file mount. SvelteKit also copies files from here during the build.
- `static/static/` is not a typo. It holds the PWA-specific assets that get referenced by `/static/` URL paths in the web app manifest.
- `static/static/custom.css` and `static/static/loader.js` are intentionally empty placeholder files. Users can populate them to override styles or inject custom scripts without modifying the codebase.
- Leaflet marker icons (`marker-icon*.png`, `marker-shadow.png`) are used by the map component and must stay at this path for Leaflet's default icon resolution.

### Testing Requirements

- Verify assets load correctly by running the dev server and checking browser network requests.
- After modifying PWA assets, test the manifest with Lighthouse or browser DevTools.
- Theme CSS files should be tested against both light and dark UI variants.

### Common Patterns

- Emoji SVGs in `assets/emojis/` are named by Unicode codepoint (e.g., `1f600.svg` for grinning face). The frontend references them by constructing the filename from the emoji's hex codepoint.
- Font files in `assets/fonts/` are loaded via CSS `@font-face` declarations. Variable fonts (Inter, Archivo, Vazirmatn) support multiple weights from a single file.
- Pyodide runtime files are loaded on demand when the Python code execution feature is activated in the browser.
- `sql-wasm.wasm` is loaded by sql.js for the built-in database query UI.

## Dependencies

### Internal

- `src/` consumes these assets at runtime via static URL paths.
- Backend (`backend/arsa/main.py`) mounts this directory as a static files route.
- SvelteKit build copies files from here into the `build/` output directory.

### External

- Pyodide (v0.28.0, Python 3.13.2 WebAssembly runtime)
- sql.js (SQLite compiled to WebAssembly)
- Leaflet (map marker icons)
- Rosé Pine color palette (theme CSS)
