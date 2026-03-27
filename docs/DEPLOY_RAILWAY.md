# Deployment Guide (Railway)

## 1. Create Services
- PostgreSQL plugin/service
- Backend service from `backend`
- Frontend service from `frontend`

## 2. Backend Service
Build:
- `pip install -r requirements.txt`

Start:
- `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Variables:
- `APP_NAME`
- `ENV=production`
- `SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `DATABASE_URL` (Railway PostgreSQL URL)
- `ORCID_API_BASE`
- `STORAGE_BACKEND`
- Optional S3 settings if enabled

## 3. Frontend Service
Build:
- `npm ci && npm run build`

Start:
- `npm run start`

Variable:
- `NEXT_PUBLIC_API_URL=https://<backend-domain>/api`

## 4. Verify Production
- Frontend reachable
- Backend `/health` OK
- DB migrations applied
- Auth flow works
- CSV/PDF exports work

## 5. Operational Recommendations
- Enable Railway logs and alerts
- Configure scheduled DB backups
- Keep staging and production environments separated
