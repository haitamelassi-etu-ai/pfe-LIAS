# Traceability Matrix (Cahier des Charges -> Implementation)

## Public Institutional Site
- Requirement: Public pages (home, publications, events, news, contact)
- Implementation:
  - `frontend/app/page.tsx`
  - `frontend/app/publications/page.tsx`
  - `frontend/app/contact/page.tsx`
  - `backend/app/api/routes/public.py`

## Member Accounts and Profiles
- Requirement: Registration, login, profile management, roles
- Implementation:
  - `backend/app/api/routes/auth.py`
  - `backend/app/api/routes/members.py`
  - `backend/app/models/user.py`

## ORCID Integration
- Requirement: ORCID link and publication import
- Implementation:
  - `backend/app/api/routes/orcid.py`
  - `backend/app/services/orcid.py`
  - `frontend/app/dashboard/page.tsx`

## Scientific Production Management
- Requirement: Publications and communications CRUD
- Implementation:
  - `backend/app/api/routes/publications.py`
  - `backend/app/api/routes/communications.py`
  - `backend/app/models/scientific.py`

## Events, News, Projects, Axes
- Requirement: Admin content management
- Implementation:
  - `backend/app/api/routes/events.py`
  - `backend/app/api/routes/news.py`
  - `backend/app/api/routes/projects.py`
  - `backend/app/api/routes/axes.py`

## Validation Workflow
- Requirement: Pending/validated/rejected lifecycle
- Implementation:
  - `backend/app/api/routes/moderation.py`
  - `backend/app/api/routes/validations.py`
  - `backend/app/models/scientific.py` (`ValidationStatus`, `Validation`)

## Search and Dashboards
- Requirement: Multicriteria search + member/admin KPIs
- Implementation:
  - `backend/app/api/routes/search.py`
  - `backend/app/api/routes/dashboard.py`
  - `frontend/app/search/page.tsx`
  - `frontend/app/admin/page.tsx`

## Exports and Reporting
- Requirement: CSV/PDF exports
- Implementation:
  - `backend/app/api/routes/exports.py`

## File Storage
- Requirement: Local storage V1 + S3-compatible option
- Implementation:
  - `backend/app/services/storage.py`
  - `backend/app/api/routes/documents.py`
  - `backend/app/core/config.py`

## Architecture and Quality
- Requirement: 3-layer architecture, maintainability, testing, CI
- Implementation:
  - `docs/ARCHITECTURE.md`
  - `backend/tests/*`
  - `.github/workflows/ci.yml`
  - `backend/alembic/*`
