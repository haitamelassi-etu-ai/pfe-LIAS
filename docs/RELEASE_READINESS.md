# Release Readiness Checklist

Use this checklist before every demo, jury presentation, or production release.

## 1. Source Control
- [ ] Default branch is `main`.
- [ ] Branch protection enabled on `main`.
- [ ] Required checks enabled:
  - [ ] Backend Quality
  - [ ] Frontend Quality
- [ ] No direct pushes to protected branch.

## 2. CI Quality Gates
- [ ] Latest workflow run is green on GitHub Actions.
- [ ] Backend tests pass.
- [ ] Frontend lint/build pass.
- [ ] CI artifacts are generated.

## 3. Database and Migrations
- [ ] `alembic upgrade head` applied in target environment.
- [ ] Seed data loaded for demo when needed.
- [ ] DB backup and restore tested.

## 4. Security and Config
- [ ] `SECRET_KEY` is strong and environment-specific.
- [ ] Production credentials are not hardcoded.
- [ ] `.env` files are not committed.
- [ ] ORCID and storage configuration validated.

## 5. Functional Smoke Test
- [ ] Public homepage loads.
- [ ] Registration and login work.
- [ ] Member dashboard loads.
- [ ] ORCID link/import works.
- [ ] Publication/communication CRUD works.
- [ ] Moderation queue works.
- [ ] CSV and PDF exports work.
- [ ] Document upload/download works.

## 6. Deployment
- [ ] Frontend URL reachable.
- [ ] Backend health endpoint returns OK.
- [ ] CORS configured for public frontend URL.
- [ ] Monitoring/logging accessible.

## 7. Soutenance Assets
- [ ] Demo scenario rehearsed.
- [ ] Screenshots and evidence prepared.
- [ ] Requirement traceability matrix updated.
- [ ] UML and architecture docs up to date.
