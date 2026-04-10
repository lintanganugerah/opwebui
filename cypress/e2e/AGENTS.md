<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-10 | Updated: 2026-04-10 -->

# e2e

## Purpose

Cypress end-to-end test specifications for Open WebUI. Each file covers a distinct feature area: chat interactions with Ollama models, user registration and login, settings management, and document handling. Specs run against a live Open WebUI instance at `localhost:8080` and exercise real UI flows using a combination of aria-label selectors, CSS classes, and button text matching.

## Key Files

| File | Description |
|------|-------------|
| `chat.cy.ts` | Chat flow tests grouped under an Ollama context: model selection from the dropdown, text chat with response waiting, chat sharing via the context menu and `/api/v1/chats/**/share` endpoint, and image generation with a 60-second timeout. Uses 10-second timeout for assistant response appearance and 120-second timeout for full generation completion |
| `registration.cy.ts` | User registration and login tests. Registers a new user with a timestamped email, verifies the pending state ("Check Again"). Also tests admin login with changelog dismissal logic. Imports `adminUser` from `../support/e2e` |
| `settings.cy.ts` | Settings page tests covering six tabs: General, Interface, Audio, Chats, Account, and About. Each test opens its respective modal and, where applicable, clicks Save. Navigates to settings via the User Menu button |
| `documents.cy.ts` | Stub file containing only the triple-slash type reference to `../support/index.d.ts`. No test cases implemented yet |

## Subdirectories

No subdirectories. All spec files sit directly in this folder.

## For AI Agents

### Working In This Directory

- Every spec file starts with a `/// <reference path="../support/index.d.ts" />` directive to pull in custom Cypress command types.
- The `after()` hook at the top of each spec waits 2 seconds (`cy.wait(2000)`) so Cypress video recording doesn't clip the final frames.
- `beforeEach()` typically calls `cy.loginAdmin()` followed by `cy.visit('/')` to reset to a known authenticated state. The registration spec is the exception: it only visits `/` without logging in.
- Selectors mix `aria-label` attributes (`button[aria-label="Select a model"]`), `data-cy` attributes (`img[data-cy="image"]`), CSS classes (`.chat-user`, `.chat-assistant`), `aria-roledescription` (`button[aria-roledescription="model-item"]`), and plain text matching (`cy.contains('Sign up')`).
- Timeouts are tuned for CI: 10 seconds for first assistant token, 120 seconds for full generation, 60 seconds for image generation.
- The `chat.cy.ts` describe block is labeled "Settings" in its `describe()` call, which is a naming inconsistency. The tests inside are chat-related.
- `registration.cy.ts` assumes no pre-existing users (or that the admin user is already an admin) and that the default role for new sign-ups is "pending".
- `documents.cy.ts` is a placeholder. If you add document tests here, also add any custom commands to `../support/e2e.ts` and their type signatures to `../support/index.d.ts`.

### Testing Requirements

- Run with `npm run cy:open` (interactive mode) or `npx cypress run` (headless).
- A running Open WebUI instance with an Ollama connection is required for `chat.cy.ts` tests to pass.
- The registration spec needs either a clean database or an environment where the admin user already exists with admin privileges.

### Common Patterns

- `describe()` wraps all tests in a block named after the feature area. `context()` further groups related tests (e.g., the Ollama context in `chat.cy.ts`).
- `beforeEach()` resets state via `cy.loginAdmin()` + `cy.visit('/')`.
- Network interception with `cy.intercept()` is used for verifying API calls (e.g., the share endpoint in the chat sharing test).
- `cy.getAllLocalStorage()` is used for conditional logic, such as dismissing the changelog dialog only when the version key is absent.
- Timestamped email addresses (`cypress-${Date.now()}@example.com`) prevent collision between test runs.

## Dependencies

### Internal

- `../support/e2e.ts`: Custom Cypress commands (`loginAdmin`, `login`, `register`, `registerAdmin`) and admin user auto-registration. Specs import `adminUser` from here.
- `../support/index.d.ts`: TypeScript type declarations for all custom commands.
- `cypress.config.ts` at repo root: Base URL (`localhost:8080`), video recording settings.
- `../data/example-doc.txt`: Test fixture for document upload (referenced by `documents.cy.ts` once implemented).
- `src/` routes: Tests navigate to SvelteKit routes (`/`, `/auth`) and interact with the rendered Svelte components.
- `backend/` API: Tests call REST endpoints including `/api/v1/auths/signup`, `/api/v1/auths/`, and `/api/v1/chats/**/share`.

### External

- Cypress: End-to-end testing framework (dev dependency in `package.json`).
