# 01-fun-facts-ui

A minimal React + Vite frontend that calls the deployed fun-facts backend and displays 5 facts for a topic.

## What this app does

- Lets you enter a topic (default is `space`)
- Calls the backend endpoint:
  - `GET https://adk-poc-lab-production.up.railway.app/fun-fact?topic=<topic>`
- Shows loading, error, and success states
- Renders returned facts as a numbered list

## How it connects to the backend

The backend base URL lives in:

- `src/config.js` → `BACKEND_BASE_URL`

The app builds a request to `/fun-fact` with a `topic` query parameter in `src/App.jsx`.

If your backend URL changes later, update `BACKEND_BASE_URL`.

## Local development

From this folder (`frontend/01-fun-facts-ui`):

```bash
npm install
npm run dev
```

Then open the local URL shown by Vite (usually `http://localhost:5173`).

## Build for production

```bash
npm run build
npm run preview
```

## Deploy to Vercel

This is a standard Vite React app, so no custom `vercel.json` is needed.

### Option 1: Vercel dashboard

1. Push this repository to GitHub.
2. In Vercel, create a new project from the repo.
3. Set the project root directory to:
   - `frontend/01-fun-facts-ui`
4. Vercel should auto-detect Vite.
5. Deploy.

### Option 2: Vercel CLI

From this folder:

```bash
npm i -g vercel
vercel
```

When prompted, set the project root to `frontend/01-fun-facts-ui`.

---

This POC is intentionally simple to show how a small frontend can call an ADK-style backend endpoint directly.
