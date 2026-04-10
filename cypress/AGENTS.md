<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-10 | Updated: 2026-04-10 -->

# cypress

## Purpose

End-to-end test suite for Open WebUI using Cypress. Tests cover the core user flows: registration and login, chat with Ollama models, settings management, and document handling. The suite is configured to run against a local instance at `localhost:8080` with video recording enabled.

## Key Files

| File | Description |
|------|-------------|
| `tsconfig.json` | TypeScript config extending the root `tsconfig.json`, with inline source maps for debugging |
| `e2e/chat.cy.ts` | Chat flow tests: model selection, text chat, chat sharing, and image generation via Ollama |
| `e2e/registration.cy.ts` | User registration and login tests, including new user sign-up and admin login |
| `e2e/settings.cy.ts` | Settings page tests: General, Interface, Audio, Chats, Account, and About modals |
| `e2e/documents.cy.ts` | Document handling tests (placeholder, references the custom command type declarations) |
| `support/e2e.ts` | Custom Cypress commands and test bootstrap. Registers the admin user before all tests, provides `login`, `register`, `loginAdmin`, and `registerAdmin` commands |
| `support/index.d.ts` | TypeScript type declarations for custom Cypress commands (`login`, `register`, `registerAdmin`, `loginAdmin`, `uploadTestDocument`, `deleteTestDocument`) |
| `data/example-doc.txt` | Sample text file (Lorem ipsum) used as test fixture for document upload tests |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `e2e/` | End-to-end test spec files, one per feature area |
| `support/` | Cypress support files: custom commands, type declarations, and test setup |
| `data/` | Test fixtures and sample data files |

## For AI Agents

### Working In This Directory

- All test files use TypeScript (`.cy.ts`). They reference custom type declarations via `/// <reference path="../support/index.d.ts" />`.
- Custom Cypress commands are defined in `support/e2e.ts`. If you add new commands, also add their type signatures to `support/index.d.ts`.
- The admin user credentials are hardcoded in `support/e2e.ts`: email `admin@example.com`, password `password`. The `before()` hook in that file auto-registers the admin before the test suite runs.
- The `loginAdmin` command uses `cy.session()` to cache authentication state between tests, reducing test time.
- Tests assume the app is running at `http://localhost:8080` (configured in `cypress.config.ts` at the repo root).
- Tests force the locale to `en-US` via `localStorage` to keep selectors stable across language settings.
- The `after()` hook in each spec waits 2 seconds to prevent Cypress from cutting off the final frames of video recordings.

### Testing Requirements

- Run tests with `npm run cy:open` (interactive) or `npx cypress run` (headless CI mode).
- A running Open WebUI instance with Ollama connected is required for chat tests to pass.
- Video is enabled by default; output goes to `cypress/videos/`.

### Common Patterns

- Each spec file wraps tests in a `describe()` block named after the feature area.
- `beforeEach()` typically calls `cy.loginAdmin()` and `cy.visit('/')` to start from a known authenticated state.
- Selectors use a mix of `aria-label` attributes, `data-cy` attributes, CSS classes, and button text content.
- Timeouts vary: 10 seconds for assistant response to appear, 120 seconds for full generation to complete, 60 seconds for image generation.
- The `documents.cy.ts` file is currently a stub with only the type reference header.

## Dependencies

### Internal

- `cypress.config.ts` at repo root: Cypress configuration (base URL, video settings).
- `tsconfig.json` at repo root: Base TypeScript configuration extended by the Cypress-specific config.
- `src/` routes: Tests navigate to SvelteKit routes (`/`, `/auth`) and interact with the rendered UI.
- `backend/` API: Tests call REST endpoints like `/api/v1/auths/signup` and `/api/v1/auths/` for setup and validation.

### External

- Cypress: End-to-end testing framework (installed as a dev dependency via `package.json`).
