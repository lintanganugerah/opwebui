# Pemetaan branding OpenWebUI di project

## Ringkasan cepat
Branding **Open WebUI** di repo ini tersebar di 5 area utama:

1. **Sumber nama aplikasi**: backend dan frontend sama-sama punya default brand `Open WebUI`.
2. **Aset visual**: favicon, logo, splash screen, manifest PWA, dan opensearch.
3. **UI frontend**: title tab, halaman auth, sidebar, about/settings, notification title, link komunitas.
4. **Backend / integrasi eksternal**: FastAPI title, header untuk OpenRouter, webhook avatar/icon, user-agent, dan error message.
5. **Legal / metadata paket**: `LICENSE`, `package.json`, `pyproject.toml`, docker/image naming.

## Titik paling penting

### 1) Nama brand utama
- `backend/open_webui/env.py:128-130`
  - Default backend name berasal dari env `WEBUI_NAME`, fallback ke `Open WebUI`.
  - Jika diubah, backend akan mengubah tampilannya menjadi `NamaKustom (Open WebUI)`.
- `src/lib/constants.ts:4`
  - Default frontend constant `APP_NAME = 'Open WebUI'`.
- `src/lib/stores/index.ts:13`
  - Store global `WEBUI_NAME` diinisialisasi dari `APP_NAME`.
- `src/routes/+layout.svelte:936`
  - Saat app boot, frontend overwrite store dengan `backendConfig.name` dari backend.

### 2) Title, metadata, dan branding browser/PWA
- `src/app.html:5-26`
  - Referensi favicon, svg icon, apple-touch-icon, dan manifest.
- `src/app.html:89-106`
  - Splash screen awal memakai `/static/splash.png` atau `/static/splash-dark.png`.
- `src/app.html:106`
  - Hardcoded `<title>Open WebUI</title>` sebagai title awal sebelum Svelte hydrate.
- `src/routes/+layout.svelte:1033-1041`
  - `<title>{$WEBUI_NAME}</title>`, description, apple-mobile-web-app-title, dan opensearch memakai nama brand runtime.
- `static/opensearch.xml:2-6`
  - `ShortName` dan `Description` masih hardcoded `Open WebUI`.
- `static/static/site.webmanifest:2`
  - Nama manifest statis masih `Open WebUI`.
- `backend/open_webui/main.py:2456-2482`
  - Endpoint manifest dinamis mengembalikan `name`, `short_name`, `description`, dan icon `/static/logo.png` memakai `app.state.WEBUI_NAME`.

### 3) Aset visual utama
File-file aset branding utama ada di dua lokasi yang isinya tampak duplikat:

- Frontend/static:
  - `static/favicon.png`
  - `static/static/favicon.png`
  - `static/static/favicon-dark.png`
  - `static/static/logo.png`
  - `static/static/splash.png`
  - `static/static/splash-dark.png`
  - `static/static/favicon.svg`
  - `static/static/favicon.ico`
  - `static/static/apple-touch-icon.png`
  - `static/static/web-app-manifest-192x192.png`
  - `static/static/web-app-manifest-512x512.png`
- Backend static:
  - `backend/open_webui/static/favicon.png`
  - `backend/open_webui/static/favicon-dark.png`
  - `backend/open_webui/static/logo.png`
  - `backend/open_webui/static/splash.png`
  - `backend/open_webui/static/splash-dark.png`
  - `backend/open_webui/static/favicon.svg`
  - `backend/open_webui/static/favicon.ico`
  - `backend/open_webui/static/apple-touch-icon.png`
  - `backend/open_webui/static/web-app-manifest-192x192.png`
  - `backend/open_webui/static/web-app-manifest-512x512.png`
  - `backend/open_webui/static/site.webmanifest`

Catatan:
- Hash menunjukkan beberapa aset frontend/backend identik untuk `favicon.png`, `logo.png`, `splash.png`, `favicon-dark.png`, dan `splash-dark.png`.
- `backend/open_webui/config.py:863-870` menyalin `frontend/static/splash.png` ke backend static saat build/runtime tertentu.

### 4) Halaman/login yang sangat terlihat user
- `src/routes/auth/+page.svelte:239-246`
  - Logo login memakai `/static/favicon.png`.
- `src/routes/auth/+page.svelte:260-272`
  - Teks onboarding/sign-in/sign-up memakai `WEBUI_NAME`.
- `src/routes/auth/+page.svelte:589-596`
  - Fallback logo login juga memakai `/static/favicon.png`.
- `src/lib/components/app/AppSidebar.svelte:58-60`
  - Sidebar app memakai favicon sebagai logo.
- `src/lib/components/layout/Sidebar.svelte:716`, `:911`, `:922`
  - Sidebar memakai favicon + menampilkan `{$WEBUI_NAME}`.
- `src/lib/components/OnBoarding.svelte:49-51`
  - Onboarding memakai `/static/favicon.png`, dark mode pakai `/static/favicon-dark.png`.

### 5) Halaman/about/settings yang masih hardcoded Open WebUI
- `src/lib/components/chat/Settings/About.svelte:117-161`
  - Ada cek `!$WEBUI_NAME.includes('Open WebUI')`, copyright Open WebUI Inc, link license, link github/twitter/openwebui.com.
- `src/lib/components/admin/Settings/General.svelte:209-282`
  - Banyak link docs/enterprise/social Open WebUI.
- `src/routes/+layout.svelte:457`, `:660`
  - Judul browser notification masih memakai suffix hardcoded `• Open WebUI`.
- `src/lib/components/channel/Channel.svelte:291-294`
  - `<title>` channel masih hardcoded `• Open WebUI`.

### 6) Backend / integrasi luar yang membawa branding
- `backend/open_webui/main.py:712`
  - FastAPI app title = `Open WebUI`.
- `backend/open_webui/routers/openai.py:155-156`
  - Untuk OpenRouter, header mengirim `HTTP-Referer: https://openwebui.com/` dan `X-Title: Open WebUI`.
- `backend/open_webui/utils/webhook.py:36-42`
  - Teams webhook memakai `activityImage = WEBUI_FAVICON_URL`.
- `backend/open_webui/env.py:132`
  - `WEBUI_FAVICON_URL = 'https://openwebui.com/favicon.png'`.
- `backend/open_webui/retrieval/web/*.py`
  - Beberapa User-Agent bertuliskan `Open WebUI (...github...) RAG Bot`.
- `backend/open_webui/routers/ollama.py`, `openai.py`, `audio.py`
  - Banyak error message: `Open WebUI: Server Connection Error`.

### 7) Mekanisme branding/custom branding bawaan
- `backend/open_webui/config.py:884-910`
  - Env legacy `CUSTOM_NAME` akan fetch branding dari `https://api.openwebui.com/api/v1/custom/{CUSTOM_NAME}`.
  - Bisa overwrite `favicon.png`, `splash.png`, dan `WEBUI_NAME`.
- `backend/open_webui/main.py:2160-2163`
  - `license metadata` expose `login_footer` dan `auth_logo_position` ke frontend.
- `src/routes/auth/+page.svelte:239`
  - `auth_logo_position` memengaruhi posisi logo di halaman auth.

### 8) Legal
- `LICENSE:18-20`
  - Lisensi repo ini secara eksplisit membatasi perubahan branding “Open WebUI”, kecuali pada kondisi tertentu.

## Area besar yang juga mengandung branding
- `src/lib/i18n/locales/**/translation.json`
  - Banyak string terjemahan mengandung `Open WebUI`, `OpenWebUI`, dan link komunitas.
- Metadata paket/deploy:
  - `package.json:2`
  - `pyproject.toml:2-3`
  - `docker-compose.yaml:15-16`
  - `run.sh:3-4`

## Kesimpulan praktis
Kalau tujuanmu adalah **rebrand penuh**, minimal area yang harus diaudit adalah:
1. `backend/open_webui/env.py`
2. `src/lib/constants.ts`
3. `src/routes/+layout.svelte`
4. `src/app.html`
5. `src/routes/auth/+page.svelte`
6. `src/lib/components/chat/Settings/About.svelte`
7. `src/lib/components/admin/Settings/General.svelte`
8. seluruh aset di `static/static/*` dan `backend/open_webui/static/*`
9. seluruh string terjemahan di `src/lib/i18n/locales/**`
10. file legal/licensing sebelum perubahan branding dilakukan
