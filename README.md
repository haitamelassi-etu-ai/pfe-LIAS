# LIAS Platform - Fullstack MVP

Plateforme web institutionnelle et scientifique du laboratoire LIAS.

## Stack
- Frontend: Next.js 14 + TypeScript
- Backend: FastAPI + SQLAlchemy
- Base de donnees: PostgreSQL
- Deploiement local: Docker Compose

## Alignement avec les technologies suggerees
- Frontend: Next.js (React.js)
- Backend: FastAPI
- Base: PostgreSQL
- Stockage fichiers: local en V1 et S3-compatible en option (configuration)

## Modules couverts
- Site public: accueil, actualites, evenements, publications validees
- Comptes membres: inscription, connexion, profil
- Espace membre: dashboard, liaison ORCID, import publications ORCID
- Gestion scientifique: publications, communications
- Administration: axes, projets, evenements, actualites, validation
- Recherche multicritere
- Tableaux de bord membre/admin
- Contact public avec boite de reception admin
- Exports CSV des publications (global et par membre)
- Exports PDF (bilan membre et bilan laboratoire)
- File de moderation des contenus en attente
- Recuperation et changement de mot de passe
- Gestion de documents (upload/download local ou S3)

## Structure
- backend/: API FastAPI, logique metier, auth JWT, ORCID
- frontend/: interface web Next.js
- docker-compose.yml: orchestration locale

## Lancer avec Docker
1. Copier les variables backend
   - cp backend/.env.example backend/.env
2. Lancer la stack
   - docker compose up --build
3. Ouvrir
   - Frontend: http://localhost:3000
   - Backend docs: http://localhost:8000/docs

## Lancer sans Docker
### Backend
1. cd backend
2. python -m venv .venv
3. .venv\\Scripts\\activate
4. pip install -r requirements.txt
5. copier .env.example vers .env
6. alembic upgrade head
7. python scripts/seed.py
8. uvicorn app.main:app --reload
7. (option demo) python scripts/seed.py

### Frontend
1. cd frontend
2. npm install
3. copier .env.example vers .env.local
4. npm run dev

## Migrations
- Initialiser/mettre a jour la base:
   - `alembic upgrade head`
- Retour arriere d'une revision:
   - `alembic downgrade -1`

## Tests backend
- Lancer les tests:
   - `pytest`
- Fichiers de tests:
   - `tests/test_auth.py`
   - `tests/test_documents_and_exports.py`

## CI GitHub Actions
- Workflow: `.github/workflows/ci.yml`
- Declenchement: push, pull request, execution manuelle
- Jobs executes:
   - Backend Quality (compile sanity + `pytest` + coverage XML + JUnit XML)
   - Frontend Quality (`npm ci` + `npm run lint` + `npm run build`)
- Artefacts CI:
   - resultats de tests backend
   - sortie build frontend

## Protection de branche
- Recommandations GitHub: `docs/BRANCH_PROTECTION.md`
- Checks a exiger avant merge:
   - `Backend Quality`
   - `Frontend Quality`

## Comptes
- Inscription: /register
- Connexion: /login

Pour creer un administrateur, inscrire un compte puis modifier son role en base (`users.role = admin`).

## API principale
- Auth: /api/auth/register, /api/auth/login, /api/auth/me
- Auth mot de passe: /api/auth/forgot-password, /api/auth/reset-password, /api/auth/change-password
- Membres: /api/members
- Publications: /api/publications
- Communications: /api/communications
- Axes: /api/axes
- Projets: /api/projects
- Evenements: /api/events
- Actualites: /api/news
- Dashboards: /api/dashboard/member, /api/dashboard/admin
- Recherche: /api/search
- ORCID: /api/orcid/link, /api/orcid/import-publications
- Public: /api/public/home
- Contact: /api/contact
- Moderation: /api/moderation/queue
- Exports: /api/exports/publications.csv, /api/exports/members/{member_id}/publications.csv
- Exports PDF: /api/exports/members/{member_id}/report.pdf, /api/exports/lab/summary.pdf
- Documents: /api/documents/upload, /api/documents/my, /api/documents/{id}/download
- Validations: /api/validations

## Soutenance PFE
- Diagrammes et architecture: docs/ARCHITECTURE.md et docs/UML_MERMAID.md
- Donnees de demonstration: backend/scripts/seed.py
- Scenario de demonstration: docs/DEMO_SCENARIO.md

## Notes
- Ce MVP couvre les fonctions critiques du cahier des charges avec une base evolutive.
- La gestion des migrations SQL (Alembic), l'export PDF avance, et les workflows multi-niveaux sont a prevoir en V2.
