from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.scientific import Axis
from app.models.user import User
from app.schemas.scientific import AxisIn, AxisOut

router = APIRouter(prefix="/axes", tags=["axes"])


@router.get("", response_model=list[AxisOut])
def list_axes(db: Session = Depends(get_db)) -> list[Axis]:
    return list(db.scalars(select(Axis).order_by(Axis.title)).all())


@router.post("", response_model=AxisOut)
def create_axis(
    payload: AxisIn,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> Axis:
    axis = Axis(**payload.model_dump())
    db.add(axis)
    db.commit()
    db.refresh(axis)
    return axis


@router.patch("/{axis_id}", response_model=AxisOut)
def update_axis(
    axis_id: int,
    payload: AxisIn,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> Axis:
    axis = db.get(Axis, axis_id)
    if not axis:
        raise HTTPException(status_code=404, detail="Axis not found")
    for key, value in payload.model_dump().items():
        setattr(axis, key, value)
    db.add(axis)
    db.commit()
    db.refresh(axis)
    return axis


@router.delete("/{axis_id}")
def delete_axis(
    axis_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> dict[str, bool]:
    axis = db.get(Axis, axis_id)
    if not axis:
        raise HTTPException(status_code=404, detail="Axis not found")
    db.delete(axis)
    db.commit()
    return {"deleted": True}
