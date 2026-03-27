from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.scientific import News
from app.models.user import User
from app.schemas.scientific import NewsIn, NewsOut

router = APIRouter(prefix="/news", tags=["news"])


@router.get("", response_model=list[NewsOut])
def list_news(db: Session = Depends(get_db), published_only: bool = False) -> list[News]:
    stmt = select(News)
    if published_only:
        stmt = stmt.where(News.is_published.is_(True))
    return list(db.scalars(stmt.order_by(News.id.desc())).all())


@router.post("", response_model=NewsOut)
def create_news(
    payload: NewsIn,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> News:
    item = News(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{news_id}", response_model=NewsOut)
def update_news(
    news_id: int,
    payload: NewsIn,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> News:
    item = db.get(News, news_id)
    if not item:
        raise HTTPException(status_code=404, detail="News not found")
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{news_id}")
def delete_news(
    news_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> dict[str, bool]:
    item = db.get(News, news_id)
    if not item:
        raise HTTPException(status_code=404, detail="News not found")
    db.delete(item)
    db.commit()
    return {"deleted": True}
