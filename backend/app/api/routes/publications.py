from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.db.session import get_db
from app.models.scientific import Publication, Validation, ValidationStatus
from app.models.user import MemberProfile, User, UserRole
from app.schemas.scientific import PublicationIn, PublicationOut

router = APIRouter(prefix="/publications", tags=["publications"])


@router.get("", response_model=list[PublicationOut])
def list_publications(
    db: Session = Depends(get_db), validated_only: bool = False
) -> list[Publication]:
    stmt = select(Publication)
    if validated_only:
        stmt = stmt.where(Publication.status == ValidationStatus.VALIDATED)
    return list(db.scalars(stmt.order_by(Publication.year.desc())).all())


@router.post("", response_model=PublicationOut)
def create_publication(
    payload: PublicationIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Publication:
    member = db.scalar(select(MemberProfile).where(MemberProfile.user_id == current_user.id))
    if not member:
        raise HTTPException(status_code=404, detail="Member profile not found")
    pub = Publication(owner_id=member.id, **payload.model_dump())
    db.add(pub)
    db.commit()
    db.refresh(pub)
    return pub


@router.patch("/{publication_id}", response_model=PublicationOut)
def update_publication(
    publication_id: int,
    payload: PublicationIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Publication:
    pub = db.get(Publication, publication_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication not found")

    member = db.scalar(select(MemberProfile).where(MemberProfile.user_id == current_user.id))
    if current_user.role != UserRole.ADMIN and member and pub.owner_id != member.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    for key, value in payload.model_dump().items():
        setattr(pub, key, value)
    pub.status = ValidationStatus.PENDING
    db.add(pub)
    db.commit()
    db.refresh(pub)
    return pub


@router.post("/{publication_id}/validate")
def validate_publication(
    publication_id: int,
    status: ValidationStatus,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> dict[str, str]:
    pub = db.get(Publication, publication_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication not found")
    previous = pub.status.value if hasattr(pub.status, "value") else str(pub.status)
    pub.status = status
    db.add(pub)
    db.add(
        Validation(
            content_type="publication",
            content_id=pub.id,
            previous_status=previous,
            new_status=status.value,
            validator_user_id=admin.id,
        )
    )
    db.commit()
    return {"status": pub.status.value}


@router.delete("/{publication_id}")
def delete_publication(
    publication_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, bool]:
    pub = db.get(Publication, publication_id)
    if not pub:
        raise HTTPException(status_code=404, detail="Publication not found")

    member = db.scalar(select(MemberProfile).where(MemberProfile.user_id == current_user.id))
    if current_user.role != UserRole.ADMIN and member and pub.owner_id != member.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(pub)
    db.commit()
    return {"deleted": True}
