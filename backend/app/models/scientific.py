from enum import StrEnum

from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Table, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ValidationStatus(StrEnum):
    DRAFT = "draft"
    PENDING = "pending"
    VALIDATED = "validated"
    REJECTED = "rejected"
    NEEDS_FIX = "needs_fix"


project_members = Table(
    "project_members",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
    Column("member_id", ForeignKey("members.id"), primary_key=True),
)


class Axis(Base):
    __tablename__ = "axes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    manager_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    members: Mapped[list["MemberProfile"]] = relationship(secondary="member_axes", back_populates="axes")


class Publication(Base):
    __tablename__ = "publications"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    axis_id: Mapped[int | None] = mapped_column(ForeignKey("axes.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(500))
    authors: Mapped[str] = mapped_column(String(1000))
    publication_type: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(index=True)
    venue: Mapped[str | None] = mapped_column(String(255), nullable=True)
    abstract: Mapped[str | None] = mapped_column(Text(), nullable=True)
    keywords: Mapped[str | None] = mapped_column(String(500), nullable=True)
    doi: Mapped[str | None] = mapped_column(String(200), nullable=True)
    external_link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    pdf_link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[ValidationStatus] = mapped_column(default=ValidationStatus.PENDING)


class Communication(Base):
    __tablename__ = "communications"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    title: Mapped[str] = mapped_column(String(500))
    authors: Mapped[str] = mapped_column(String(1000))
    event_name: Mapped[str] = mapped_column(String(255))
    communication_type: Mapped[str] = mapped_column(String(100))
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    event_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    abstract: Mapped[str | None] = mapped_column(Text(), nullable=True)
    communication_status: Mapped[str] = mapped_column(String(50), default="submitted")
    document_link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    validation_status: Mapped[ValidationStatus] = mapped_column(default=ValidationStatus.PENDING)


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    axis_id: Mapped[int | None] = mapped_column(ForeignKey("axes.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    place: Mapped[str | None] = mapped_column(String(255), nullable=True)
    event_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    speakers: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    poster_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="upcoming")


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text())
    is_published: Mapped[bool] = mapped_column(default=False)


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    subject: Mapped[str] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(Text())
    is_processed: Mapped[bool] = mapped_column(default=False)


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    publication_id: Mapped[int | None] = mapped_column(ForeignKey("publications.id"), nullable=True)
    communication_id: Mapped[int | None] = mapped_column(ForeignKey("communications.id"), nullable=True)
    original_name: Mapped[str] = mapped_column(String(255))
    stored_name: Mapped[str] = mapped_column(String(500), unique=True)
    storage_backend: Mapped[str] = mapped_column(String(20), default="local")
    file_url: Mapped[str] = mapped_column(String(1000))
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    size_bytes: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Validation(Base):
    __tablename__ = "validations"

    id: Mapped[int] = mapped_column(primary_key=True)
    content_type: Mapped[str] = mapped_column(String(50))
    content_id: Mapped[int] = mapped_column(index=True)
    previous_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    new_status: Mapped[str] = mapped_column(String(50))
    note: Mapped[str | None] = mapped_column(Text(), nullable=True)
    validator_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    axis_id: Mapped[int | None] = mapped_column(ForeignKey("axes.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str | None] = mapped_column(Text(), nullable=True)
    manager: Mapped[str | None] = mapped_column(String(255), nullable=True)
    partners: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    funding: Mapped[str | None] = mapped_column(String(255), nullable=True)
    start_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)

    members: Mapped[list["MemberProfile"]] = relationship(secondary=project_members)


from app.models.user import MemberProfile  # noqa: E402
