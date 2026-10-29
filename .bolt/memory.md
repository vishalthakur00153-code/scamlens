# Project memory

## Product intent & audience

- ScamLens: a scam-detection web app that scans messages and URLs for fraudulent patterns and assigns risk levels (Low Concern, Needs Verification, Suspicious).
- Target users: general users checking suspicious messages/links for safety.

## Brand personality & voice

- Security-focused, clear, direct communication.
- Risk levels and scan results communicated plainly without alarmism.

## Visual design & UX direction

- Existing ScamLens design preserved; no redesign performed or implied.
- Frontend is a static site (HTML/CSS/JS) built with Vite; original styling and layout kept intact.
- API errors surfaced to user with clear "server unreachable" messaging rather than silent failures.

## Decisions, constraints & rationale

- Root cause of blank page: imported GitHub repo files were flattened into project root, destroying the `app/` (FastAPI) and `frontend/` folder structure; no build config existed for Bolt.
- Fix: restored original folder layout (`app/`, `frontend/`), added Vite build setup, removed broken Vercel config.
- Backend: Python FastAPI with scam-detection rules; all 36 backend tests restored and passing.
- Frontend API calls now route through a configurable `API_BASE_URL` (set in `frontend/app.js`) so frontend can target a separately hosted backend.
- Bolt.host cannot host Python backend; recommended Render.com (Web Service from GitHub repo, reads `render.yaml`).
- `.gitignore` edits were blocked by environment; assumed it already lists `node_modules`.
- No live browser testing or scan verification was possible; frontend builds cleanly but runtime behavior unconfirmed.

## Open questions & assumptions

- `API_BASE_URL` must be manually set to the Render service URL and republished for Bolt-hosted frontend to reach backend.
- Live scan functionality (message + URL) remains unverified—needs browser testing after backend deployment.
- Assumes `render.yaml` is correctly configured in repo for Render to auto-detect and deploy FastAPI service.
- Assumes user will commit changes and push to GitHub to trigger Render deployment.