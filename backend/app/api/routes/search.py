from fastapi import APIRouter, Depends
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.scientific import Event, Project, Publication
from app.models.user import MemberProfile

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
def search(
    q: str,
    year: int | None = None,
    publication_type: str | None = None,
    db: Session = Depends(get_db),
) -> dict:
    members = list(
        db.scalars(
            select(MemberProfile).where(
                or_(
                    MemberProfile.first_name.ilike(f"%{q}%"),
                    MemberProfile.last_name.ilike(f"%{q}%"),
                )
            )
        ).all()
    )

    pub_stmt = select(Publication).where(Publication.title.ilike(f"%{q}%"))
    if year is not None:
        pub_stmt = pub_stmt.where(Publication.year == year)
    if publication_type:
        pub_stmt = pub_stmt.where(Publication.publication_type == publication_type)
    publications = list(db.scalars(pub_stmt).all())

    projects = list(db.scalars(select(Project).where(Project.title.ilike(f"%{q}%"))).all())
    events = list(db.scalars(select(Event).where(Event.title.ilike(f"%{q}%"))).all())

    return {
        "members": [{"id": m.id, "name": f"{m.first_name} {m.last_name}"} for m in members],
        "publications": [{"id": p.id, "title": p.title, "year": p.year} for p in publications],
        "projects": [{"id": p.id, "title": p.title} for p in projects],
        "events": [{"id": e.id, "title": e.title} for e in events],
    }
