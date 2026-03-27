from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.db.session import get_db
from app.models.scientific import Communication, Validation, ValidationStatus
from app.models.user import MemberProfile, User, UserRole
from app.schemas.scientific import CommunicationIn, CommunicationOut

router = APIRouter(prefix="/communications", tags=["communications"])


@router.get("", response_model=list[CommunicationOut])
def list_communications(db: Session = Depends(get_db)) -> list[Communication]:
    return list(db.scalars(select(Communication).order_by(Communication.id.desc())).all())


@router.post("", response_model=CommunicationOut)
def create_communication(
    payload: CommunicationIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Communication:
    member = db.scalar(select(MemberProfile).where(MemberProfile.user_id == current_user.id))
    if not member:
        raise HTTPException(status_code=404, detail="Member profile not found")
    item = Communication(owner_id=member.id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{communication_id}", response_model=CommunicationOut)
def update_communication(
    communication_id: int,
    payload: CommunicationIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Communication:
    item = db.get(Communication, communication_id)
    if not item:
        raise HTTPException(status_code=404, detail="Communication not found")

    member = db.scalar(select(MemberProfile).where(MemberProfile.user_id == current_user.id))
    if current_user.role != UserRole.ADMIN and member and item.owner_id != member.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    item.validation_status = ValidationStatus.PENDING
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.post("/{communication_id}/validate")
def validate_communication(
    communication_id: int,
    status: ValidationStatus,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> dict[str, str]:
    item = db.get(Communication, communication_id)
    if not item:
        raise HTTPException(status_code=404, detail="Communication not found")
    previous = (
        item.validation_status.value
        if hasattr(item.validation_status, "value")
        else str(item.validation_status)
    )
    item.validation_status = status
    db.add(item)
    db.add(
        Validation(
            content_type="communication",
            content_id=item.id,
            previous_status=previous,
            new_status=status.value,
            validator_user_id=admin.id,
        )
    )
    db.commit()
    return {"status": item.validation_status.value}


@router.delete("/{communication_id}")
def delete_communication(
    communication_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, bool]:
    item = db.get(Communication, communication_id)
    if not item:
        raise HTTPException(status_code=404, detail="Communication not found")

    member = db.scalar(select(MemberProfile).where(MemberProfile.user_id == current_user.id))
    if current_user.role != UserRole.ADMIN and member and item.owner_id != member.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(item)
    db.commit()
    return {"deleted": True}
