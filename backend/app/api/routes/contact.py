from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.scientific import ContactMessage
from app.models.user import User
from app.schemas.scientific import ContactMessageIn, ContactMessageOut

router = APIRouter(prefix="/contact", tags=["contact"])


@router.post("", response_model=ContactMessageOut)
def create_contact_message(payload: ContactMessageIn, db: Session = Depends(get_db)) -> ContactMessage:
    item = ContactMessage(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=list[ContactMessageOut])
def list_contact_messages(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> list[ContactMessage]:
    return list(db.scalars(select(ContactMessage).order_by(ContactMessage.id.desc())).all())


@router.post("/{message_id}/process")
def process_contact_message(
    message_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> dict[str, bool]:
    item = db.get(ContactMessage, message_id)
    if not item:
        raise HTTPException(status_code=404, detail="Message not found")
    item.is_processed = True
    db.add(item)
    db.commit()
    return {"processed": True}
