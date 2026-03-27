# Deployment Guide (Render)

## 1. Services to Create
- PostgreSQL database on Render
- Web Service for backend (FastAPI)
- Static Site or Web Service for frontend (Next.js)

## 2. Backend Deploy (Render Web Service)
Repository root: `backend`

Build command:
- `pip install -r requirements.txt`

Start command:
- `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Environment variables (minimum):
- `APP_NAME=LIAS Platform API`
- `ENV=production`
- `SECRET_KEY=<strong-random-value>`
- `ACCESS_TOKEN_EXPIRE_MINUTES=1440`
- `DATABASE_URL=<render-postgres-connection-string>`
- `ORCID_API_BASE=https://pub.orcid.org/v3.0`
- `STORAGE_BACKEND=local` or `s3`

## 3. Frontend Deploy
Repository root: `frontend`

Build command:
- `npm ci && npm run build`

Start command:
- `npm run start`

Environment variables:
- `NEXT_PUBLIC_API_URL=https://<your-backend-domain>/api`

## 4. Post-Deploy Validation
- Open frontend URL.
- Verify `GET /health` on backend.
- Test login, dashboard, and exports.
- Validate CORS (frontend can call backend).

## 5. Notes
- For persistent file storage in production, use S3-compatible backend.
- Keep secrets in Render environment settings only.
