---
name: ai-sdlc-5-deploy
description: Containerize and deploy the release; verify it actually runs, not just that it built.
---

# PHASE 5 — DEPLOY

## Steps
1. `docker build -t procurement-orchestrator .`
2. Push/connect the repo to Render as a Docker Web Service.
3. Set `DATABASE_URL` to the Neon Postgres connection string.
4. Deploy, then manually call `GET /health` and run through at least one
   full pipeline scenario against the deployed URL.

## Rules
- A successfully built Docker image or a green CI workflow is NOT evidence
  that the deployment actually works end-to-end. Verify manually.
- Update `docs/TASKS.md`: `PHASE: 5-DEPLOY`, `STATUS: done` only after the
  manual end-to-end check above has passed against the live URL.
