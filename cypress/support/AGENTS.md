<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-10 | Updated: 2026-04-10 -->

# cypress/support

## Purpose

Cypress support layer that bootstraps the test environment and provides reusable custom commands. The `before()` hook in `e2e.ts` auto-registers the admin user before any spec runs, so every test suite starts with a known user in the database.

## Key Files

| File | Description |
|------|-------------|
| `e2e.ts` | Main support file. Exports `adminUser` credentials, defines `login`, `register`, `registerAdmin`, and `loginAdmin` helper functions, registers them as Cypress custom commands, and runs `cy.registerAdmin()` in a global `before()` hook |
| `index.d.ts` | TypeScript declarations for custom commands (`login`, `register`, `registerAdmin`, `loginAdmin`, `uploadTestDocument`, `deleteTestDocument`) on the `Cypress.Chainable` interface |

## Subdirectories

This directory has no subdirectories.

## For AI Agents

### Working In This Directory

- Adding a new custom command requires changes in two places: the implementation in `e2e.ts` and the type signature in `index.d.ts`. Forgetting either breaks TypeScript checking or runtime.
- `login` wraps `cy.session()`, so calling it multiple times with the same email reuses the cached session instead of repeating the login flow. Keep this in mind when debugging auth-related test failures.
- The admin credentials (`admin@example.com` / `password`) are hardcoded here. Changing them means updating the object at the top of `e2e.ts`.
- The `validate` callback inside `login` hits `GET /api/v1/auths/` with the stored token. If that endpoint changes, this validation will break.
- Locale is forced to `en-US` inside the login session setup so that selectors remain stable regardless of browser language settings.
- The changelog dialog is dismissed automatically by clicking "Okay, Let's Go!" on first login. If the onboarding UI changes, this selector needs updating.

### Testing Requirements

- After modifying custom commands, run `npm run cy:open` and execute a spec that uses the changed command to verify it still works end to end.
- TypeScript compilation of Cypress files can be checked with `npx tsc --project cypress/tsconfig.json --noEmit`.

### Common Patterns

- Commands follow the pattern: private function that returns a Cypress chainable, then `Cypress.Commands.add()` to expose it globally.
- `register` uses `failOnStatusCode: false` and asserts the status is 200 or 400, so it works whether the user already exists or not. This makes the command idempotent.
- `loginAdmin` is a thin wrapper around `login` with the admin email and password. Other convenience wrappers should follow the same pattern.

## Dependencies

### Internal

- `../e2e/` spec files: Consume the custom commands defined here.
- `cypress.config.ts` at repo root: Provides the `baseUrl` (`http://localhost:8080`) that `cy.visit()` resolves against.
- `backend/` API endpoints: `login` calls `GET /api/v1/auths/` for session validation; `register` calls `POST /api/v1/auths/signup` to create users.

### External

- Cypress: The `Cypress.Commands.add()` API and `cy.session()` are part of the Cypress test runner, installed as a dev dependency.
