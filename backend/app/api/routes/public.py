from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.scientific import Event, News, Publication, ValidationStatus

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/home")
def home(db: Session = Depends(get_db)) -> dict:
    latest_news = list(
        db.scalars(select(News).where(News.is_published.is_(True)).order_by(News.id.desc()).limit(5)).all()
    )
    upcoming_events = list(db.scalars(select(Event).order_by(Event.id.desc()).limit(5)).all())
    latest_publications = list(
        db.scalars(
            select(Publication)
            .where(Publication.status == ValidationStatus.VALIDATED)
            .order_by(Publication.year.desc())
            .limit(10)
        ).all()
    )

    return {
        "news": [{"id": n.id, "title": n.title} for n in latest_news],
        "events": [{"id": e.id, "title": e.title, "date": e.event_date} for e in upcoming_events],
        "publications": [{"id": p.id, "title": p.title, "year": p.year} for p in latest_publications],
    }
