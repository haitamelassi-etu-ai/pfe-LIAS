from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.scientific import Communication, Document, Publication
from app.models.user import MemberProfile, User, UserRole
from app.schemas.scientific import DocumentOut
from app.services.storage import save_upload

router = APIRouter(prefix="/documents", tags=["documents"])


def _member_or_404(db: Session, user_id: int) -> MemberProfile:
    member = db.scalar(select(MemberProfile).where(MemberProfile.user_id == user_id))
    if not member:
        raise HTTPException(status_code=404, detail="Member profile not found")
    return member


@router.post("/upload", response_model=DocumentOut)
def upload_document(
    publication_id: int | None = None,
    communication_id: int | None = None,
    upload: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Document:
    member = _member_or_404(db, current_user.id)

    if publication_id is not None:
        publication = db.get(Publication, publication_id)
        if not publication:
            raise HTTPException(status_code=404, detail="Publication not found")
        if current_user.role != UserRole.ADMIN and publication.owner_id != member.id:
            raise HTTPException(status_code=403, detail="Not allowed")

    if communication_id is not None:
        communication = db.get(Communication, communication_id)
        if not communication:
            raise HTTPException(status_code=404, detail="Communication not found")
        if current_user.role != UserRole.ADMIN and communication.owner_id != member.id:
            raise HTTPException(status_code=403, detail="Not allowed")

    saved = save_upload(upload)
    item = Document(
        owner_id=member.id,
        publication_id=publication_id,
        communication_id=communication_id,
        original_name=upload.filename or "document.bin",
        stored_name=str(saved["stored_name"]),
        storage_backend=str(saved["storage_backend"]),
        file_url=str(saved["file_url"]),
        mime_type=upload.content_type,
        size_bytes=int(saved["size_bytes"]),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/my", response_model=list[DocumentOut])
def list_my_documents(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[Document]:
    member = _member_or_404(db, current_user.id)
    if current_user.role == UserRole.ADMIN:
        return list(db.scalars(select(Document).order_by(Document.id.desc())).all())
    return list(
        db.scalars(
            select(Document).where(Document.owner_id == member.id).order_by(Document.id.desc())
        ).all()
    )


@router.get("/{document_id}/download")
def download_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    member = _member_or_404(db, current_user.id)
    item = db.get(Document, document_id)
    if not item:
        raise HTTPException(status_code=404, detail="Document not found")

    if current_user.role != UserRole.ADMIN and item.owner_id != member.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    if item.storage_backend == "s3":
        return RedirectResponse(url=item.file_url)

    path = Path(item.file_url)
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found in local storage")
    return FileResponse(path=str(path), filename=item.original_name, media_type=item.mime_type)
