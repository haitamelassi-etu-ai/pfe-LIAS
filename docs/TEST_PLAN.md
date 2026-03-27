# Test Plan

## 1. Test Scope
- Backend API functional tests
- Authentication and authorization tests
- Document and export tests
- Frontend lint/build quality checks
- End-to-end manual smoke tests

## 2. Automated Backend Tests
Run from `backend`:
- `pytest`

Covered suites:
- `tests/test_auth.py`
- `tests/test_documents_and_exports.py`

## 3. Frontend Quality Checks
Run from `frontend`:
- `npm run lint`
- `npm run build`

## 4. Manual End-to-End Scenarios
### Scenario A: Public Visitor
1. Open homepage.
2. Open publications page.
3. Submit contact form.

### Scenario B: Member
1. Register account.
2. Login.
3. Link ORCID.
4. Import ORCID publications.
5. Upload and download a document.
6. Export member PDF report.

### Scenario C: Administrator
1. Login as admin.
2. Access admin dashboard.
3. Review moderation queue.
4. Validate pending content.
5. Export lab summary PDF.

## 5. Acceptance Criteria
- All automated tests pass.
- Frontend lint/build pass.
- End-to-end scenarios complete without blocking errors.
- Generated CSV/PDF documents are downloadable and readable.
