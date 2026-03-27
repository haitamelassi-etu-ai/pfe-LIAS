from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.scientific import Publication
from app.models.user import MemberProfile, User
from app.services.orcid import fetch_orcid_works

router = APIRouter(prefix="/orcid", tags=["orcid"])


@router.post("/link")
def link_orcid(
    orcid_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    member = db.scalar(select(MemberProfile).where(MemberProfile.user_id == current_user.id))
    if not member:
        raise HTTPException(status_code=404, detail="Member profile not found")
    member.orcid_id = orcid_id
    db.add(member)
    db.commit()
    return {"orcid_id": orcid_id}


@router.post("/import-publications")
async def import_publications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, int]:
    member = db.scalar(select(MemberProfile).where(MemberProfile.user_id == current_user.id))
    if not member or not member.orcid_id:
        raise HTTPException(status_code=400, detail="ORCID account not linked")

    works = await fetch_orcid_works(member.orcid_id)
    created = 0
    for work in works:
        exists = db.scalar(
            select(Publication).where(
                Publication.owner_id == member.id,
                Publication.title == work["title"],
            )
        )
        if exists:
            continue
        publication = Publication(
            owner_id=member.id,
            title=work["title"],
            authors=f"{member.first_name} {member.last_name}",
            publication_type=work["type"],
            year=work["year"] or 2000,
            doi=work.get("doi"),
            venue="Imported from ORCID",
            status="pending",
        )
        db.add(publication)
        created += 1

    db.commit()
    return {"imported": created}
