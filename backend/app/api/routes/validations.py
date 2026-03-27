from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.scientific import Validation
from app.models.user import User
from app.schemas.scientific import ValidationOut

router = APIRouter(prefix="/validations", tags=["validations"])


@router.get("", response_model=list[ValidationOut])
def list_validations(
    content_type: str | None = None,
    content_id: int | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> list[Validation]:
    stmt = select(Validation).order_by(Validation.id.desc())
    if content_type:
        stmt = stmt.where(Validation.content_type == content_type)
    if content_id is not None:
        stmt = stmt.where(Validation.content_id == content_id)
    return list(db.scalars(stmt).all())
