from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.scientific import Communication, Publication, Validation, ValidationStatus
from app.models.user import User

router = APIRouter(prefix="/moderation", tags=["moderation"])


@router.get("/queue")
def moderation_queue(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> dict:
    publications = list(
        db.scalars(select(Publication).where(Publication.status == ValidationStatus.PENDING)).all()
    )
    communications = list(
        db.scalars(
            select(Communication).where(Communication.validation_status == ValidationStatus.PENDING)
        ).all()
    )
    return {
        "publications": [{"id": p.id, "title": p.title, "year": p.year} for p in publications],
        "communications": [{"id": c.id, "title": c.title, "event": c.event_name} for c in communications],
    }


@router.post("/publications/{publication_id}")
def moderate_publication(
    publication_id: int,
    decision: ValidationStatus,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> dict[str, str]:
    item = db.get(Publication, publication_id)
    if not item:
        raise HTTPException(status_code=404, detail="Publication not found")
    previous = item.status.value if hasattr(item.status, "value") else str(item.status)
    item.status = decision
    db.add(item)
    db.add(
        Validation(
            content_type="publication",
            content_id=item.id,
            previous_status=previous,
            new_status=decision.value,
            validator_user_id=admin.id,
        )
    )
    db.commit()
    return {"status": item.status}


@router.post("/communications/{communication_id}")
def moderate_communication(
    communication_id: int,
    decision: ValidationStatus,
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
    item.validation_status = decision
    db.add(item)
    db.add(
        Validation(
            content_type="communication",
            content_id=item.id,
            previous_status=previous,
            new_status=decision.value,
            validator_user_id=admin.id,
        )
    )
    db.commit()
    return {"status": item.validation_status}
