import csv
import io

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.db.session import get_db
from app.models.scientific import Communication, Event, Publication
from app.models.user import MemberProfile, User, UserRole

router = APIRouter(prefix="/exports", tags=["exports"])


def _csv_response(filename: str, rows: list[dict[str, str | int | None]]) -> StreamingResponse:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "title", "authors", "type", "year", "doi", "status"])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


def _pdf_response(filename: str, title: str, lines: list[str]) -> StreamingResponse:
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    pdf.setTitle(title)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, title)
    y -= 30

    pdf.setFont("Helvetica", 10)
    for line in lines:
        if y < 50:
            pdf.showPage()
            y = height - 50
            pdf.setFont("Helvetica", 10)
        pdf.drawString(40, y, line[:140])
        y -= 16

    pdf.save()
    buffer.seek(0)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/publications.csv")
def export_publications_csv(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> StreamingResponse:
    publications = list(db.scalars(select(Publication).order_by(Publication.year.desc())).all())
    rows = [
        {
            "id": p.id,
            "title": p.title,
            "authors": p.authors,
            "type": p.publication_type,
            "year": p.year,
            "doi": p.doi,
            "status": p.status,
        }
        for p in publications
    ]
    return _csv_response("publications.csv", rows)


@router.get("/members/{member_id}/publications.csv")
def export_member_publications_csv(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StreamingResponse:
    if current_user.role != UserRole.ADMIN:
        me = db.scalar(select(MemberProfile).where(MemberProfile.user_id == current_user.id))
        if not me or me.id != member_id:
            raise HTTPException(status_code=403, detail="Not allowed")

    publications = list(
        db.scalars(
            select(Publication)
            .where(Publication.owner_id == member_id)
            .order_by(Publication.year.desc())
        ).all()
    )
    rows = [
        {
            "id": p.id,
            "title": p.title,
            "authors": p.authors,
            "type": p.publication_type,
            "year": p.year,
            "doi": p.doi,
            "status": p.status,
        }
        for p in publications
    ]
    return _csv_response(f"member_{member_id}_publications.csv", rows)


@router.get("/members/{member_id}/report.pdf")
def export_member_report_pdf(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StreamingResponse:
    if current_user.role != UserRole.ADMIN:
        me = db.scalar(select(MemberProfile).where(MemberProfile.user_id == current_user.id))
        if not me or me.id != member_id:
            raise HTTPException(status_code=403, detail="Not allowed")

    member = db.get(MemberProfile, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    publications = list(
        db.scalars(select(Publication).where(Publication.owner_id == member_id).order_by(Publication.year.desc())).all()
    )
    lines = [
        f"Membre: {member.first_name} {member.last_name}",
        f"Email: {member.professional_email or 'N/A'}",
        f"Total publications: {len(publications)}",
        "",
        "Liste des publications:",
    ]
    for idx, p in enumerate(publications, start=1):
        lines.append(f"{idx}. [{p.year}] {p.title} ({p.publication_type})")
    return _pdf_response(
        f"member_{member_id}_report.pdf",
        "Bilan scientifique membre",
        lines,
    )


@router.get("/lab/summary.pdf")
def export_lab_summary_pdf(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> StreamingResponse:
    members_count = db.scalar(select(func.count()).select_from(MemberProfile)) or 0
    publications_count = db.scalar(select(func.count()).select_from(Publication)) or 0
    communications_count = db.scalar(select(func.count()).select_from(Communication)) or 0
    events_count = db.scalar(select(func.count()).select_from(Event)) or 0

    lines = [
        "Bilan global du laboratoire LIAS",
        "",
        f"Nombre de membres: {members_count}",
        f"Nombre de publications: {publications_count}",
        f"Nombre de communications: {communications_count}",
        f"Nombre d'evenements: {events_count}",
    ]
    return _pdf_response("lab_summary.pdf", "Bilan global laboratoire", lines)
