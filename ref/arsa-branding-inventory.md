# Inventory lokasi branding Arsa

## A. Source of truth / config brand
- `backend/arsa/env.py:128-132` — `WEBUI_NAME`, `WEBUI_FAVICON_URL`
- `src/lib/constants.ts:4` — `APP_NAME = 'Arsa'`
- `src/lib/stores/index.ts:13` — store `WEBUI_NAME`
- `src/routes/+layout.svelte:936` — `WEBUI_NAME.set(backendConfig.name)`
- `backend/arsa/main.py:2138-2166` — backend config expose `license_metadata` & `metadata.auth_logo_position`
- `backend/arsa/config.py:884-910` — legacy custom branding via `CUSTOM_NAME`

## B. HTML shell / browser metadata / PWA
- `src/app.html:5-26` — favicon, apple-touch-icon, manifest
- `src/app.html:89-106` — splash image boot screen
- `src/app.html:106` — hardcoded initial `<title>Arsa</title>`
- `src/routes/+layout.svelte:1033-1041` — runtime `<title>`, description, apple web app title, opensearch title
- `static/opensearch.xml:2-6` — Arsa short name / description
- `static/static/site.webmanifest:2-16` — static manifest brand name
- `backend/arsa/main.py:2456-2482` — dynamic manifest payload
- `backend/arsa/static/site.webmanifest:2-16` — backend manifest copy

## C. Visual assets
### Frontend static
- `static/favicon.png`
- `static/static/apple-touch-icon.png`
- `static/static/favicon-96x96.png`
- `static/static/favicon-dark.png`
- `static/static/favicon.ico`
- `static/static/favicon.png`
- `static/static/favicon.svg`
- `static/static/logo.png`
- `static/static/splash.png`
- `static/static/splash-dark.png`
- `static/static/web-app-manifest-192x192.png`
- `static/static/web-app-manifest-512x512.png`

### Backend static
- `backend/arsa/static/apple-touch-icon.png`
- `backend/arsa/static/favicon-96x96.png`
- `backend/arsa/static/favicon-dark.png`
- `backend/arsa/static/favicon.ico`
- `backend/arsa/static/favicon.png`
- `backend/arsa/static/favicon.svg`
- `backend/arsa/static/logo.png`
- `backend/arsa/static/splash.png`
- `backend/arsa/static/splash-dark.png`
- `backend/arsa/static/swagger-ui/favicon.png`
- `backend/arsa/static/web-app-manifest-192x192.png`
- `backend/arsa/static/web-app-manifest-512x512.png`

## D. UI yang menampilkan nama/logo brand runtime
- `src/routes/auth/+page.svelte`
- `src/routes/+layout.svelte`
- `src/routes/s/[id]/+page.svelte`
- `src/lib/components/app/AppSidebar.svelte`
- `src/lib/components/layout/Sidebar.svelte`
- `src/lib/components/OnBoarding.svelte`
- `src/lib/components/chat/Chat.svelte`
- `src/lib/components/chat/Navbar.svelte`
- `src/lib/components/chat/Suggestions.svelte`
- `src/lib/components/notes/Notes.svelte`
- `src/lib/components/notes/NoteEditor.svelte`
- `src/routes/(app)/*/+layout.svelte` (title per section pakai `WEBUI_NAME`)

## E. UI yang masih hardcoded Arsa / arsa.com
- `src/lib/components/chat/Settings/About.svelte`
- `src/lib/components/admin/Settings/General.svelte`
- `src/lib/components/admin/Functions.svelte`
- `src/lib/components/workspace/Tools.svelte`
- `src/lib/components/workspace/Models.svelte`
- `src/lib/components/workspace/Prompts.svelte`
- `src/lib/components/chat/ShareChatModal.svelte`
- `src/lib/components/admin/Evaluations/Feedbacks.svelte`
- `src/lib/components/channel/Channel.svelte`
- `src/routes/+layout.svelte` (notification title suffix)
- `src/routes/error/+page.svelte`

## F. I18n / copy besar
- `src/lib/i18n/locales/**/translation.json`
  - Banyak string seperti:
    - `Sign in to {{WEBUI_NAME}}`
    - `Get started with {{WEBUI_NAME}}`
    - `Arsa version`
    - `Redirecting you to Arsa Community`
    - `Share to Arsa Community`
    - `Made by Arsa Community`

## G. Backend / integration branding
- `backend/arsa/main.py:712` — FastAPI title
- `backend/arsa/env.py:132` — remote favicon URL
- `backend/arsa/utils/webhook.py:36-42` — webhook card image
- `backend/arsa/routers/openai.py:155-156` — OpenRouter referer/title
- `backend/arsa/retrieval/web/external.py:27`
- `backend/arsa/retrieval/web/searxng.py:68`
- `backend/arsa/retrieval/web/yacy.py:62`
- `backend/arsa/retrieval/web/yandex.py:45`
- `backend/arsa/retrieval/loaders/external_web.py:33`
- `backend/arsa/routers/ollama.py` — error copy
- `backend/arsa/routers/openai.py` — error copy
- `backend/arsa/routers/audio.py` — error copy

## H. Package/deploy/legal
- `package.json:2`
- `package-lock.json:2`
- `pyproject.toml:2-5`
- `uv.lock`
- `docker-compose.yaml:15-16`
- `docker-compose.otel.yaml:16-17`
- `run.sh:3-4`
- `LICENSE:18-20`
- `LICENSE_NOTICE:1-9`

## Statistik kasar hasil eksplorasi
- File locale yang mengandung branding: 60 file
- File UI langsung (tanpa locales) yang mengandung branding: 37 file
- File backend langsung yang mengandung branding: 31 file

## Catatan
Dokumen ini fokus ke **lokasi branding**. Ia belum mengubah apa pun.
