---
name: ai-sdlc-5-deploy
description: Prepare and verify delivery of a validated artifact.
---

# 5 DEPLOY — Is delivery prepared or executed?

1. Deploy only a validated artifact. Agree the target (Render + Neon) with the team.
2. Configure `.github/workflows/cd.yml` (inactive until repo variable `CD_ENABLED=true`), document secrets by name only, trigger, smoke check and rollback.
3. Set `DATABASE_URL` on the target; never commit secret values.
4. After an authorized run, call `GET /health` and one full pipeline scenario on the live URL.

A verified workflow is not proof of a deployment: record the actual deployment and smoke-test result separately. Feedback goes back to SPECIFY. Record `PHASE: 5`.
