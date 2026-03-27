from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.db.session import get_db
from app.models.scientific import Communication, Event, Publication
from app.models.user import MemberProfile, User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/member")
def member_dashboard(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> dict:
    member = db.scalar(select(MemberProfile).where(MemberProfile.user_id == current_user.id))
    if not member:
        return {"profile": None, "publications": 0, "communications": 0}

    pub_count = db.scalar(select(func.count()).where(Publication.owner_id == member.id)) or 0
    com_count = db.scalar(select(func.count()).where(Communication.owner_id == member.id)) or 0

    return {
        "profile": {
            "id": member.id,
            "name": f"{member.first_name} {member.last_name}",
            "orcid_id": member.orcid_id,
        },
        "publications": pub_count,
        "communications": com_count,
    }


@router.get("/admin")
def admin_dashboard(
    db: Session = Depends(get_db), _: User = Depends(require_admin)
) -> dict:
    members = db.scalar(select(func.count()).select_from(MemberProfile)) or 0
    publications = db.scalar(select(func.count()).select_from(Publication)) or 0
    communications = db.scalar(select(func.count()).select_from(Communication)) or 0
    events = db.scalar(select(func.count()).select_from(Event)) or 0

    return {
        "members": members,
        "publications": publications,
        "communications": communications,
        "events": events,
    }
