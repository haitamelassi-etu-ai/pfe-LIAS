# Architecture Technique LIAS

## Vue globale
Architecture en 3 couches:
- Frontend Next.js
- Backend FastAPI
- Base PostgreSQL

## Modules backend
- Authentification et roles (JWT)
- Gestion membres et profils
- Publications et communications
- Projets, axes, actualites, evenements
- Workflow de moderation
- Exports CSV
- ORCID (liaison + import)
- Contact public
- Documents (upload/download)
- Tracabilite des validations

## Base de donnees PostgreSQL
Entites principales stockees:
- utilisateurs
- profils membres
- publications
- communications
- evenements
- actualites
- projets
- axes de recherche
- documents
- validations

## Stockage de fichiers
- V1: stockage local (dossier configure par `LOCAL_STORAGE_PATH`)
- Option evolutive: stockage objet compatible S3 (`STORAGE_BACKEND=s3`)

## Principes qualite
- Separation claire routes/services/models
- Typage fort Pydantic + SQLAlchemy
- Controle d'acces par role
- APIs REST coherentes
- Structure monorepo maintenable
