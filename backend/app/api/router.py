from fastapi import APIRouter

from app.api.routes import (
    auth,
    axes,
    communications,
    contact,
    dashboard,
    documents,
    events,
    exports,
    members,
    moderation,
    news,
    orcid,
    projects,
    public,
    publications,
    search,
    validations,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(members.router)
api_router.include_router(axes.router)
api_router.include_router(publications.router)
api_router.include_router(communications.router)
api_router.include_router(contact.router)
api_router.include_router(documents.router)
api_router.include_router(events.router)
api_router.include_router(news.router)
api_router.include_router(projects.router)
api_router.include_router(exports.router)
api_router.include_router(moderation.router)
api_router.include_router(search.router)
api_router.include_router(dashboard.router)
api_router.include_router(orcid.router)
api_router.include_router(public.router)
api_router.include_router(validations.router)
