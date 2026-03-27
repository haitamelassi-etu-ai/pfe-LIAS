from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import Column, Enum, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.scientific import Axis


class UserRole(StrEnum):
    MEMBER = "member"
    DOCTORANT = "doctorant"
    ADMIN = "admin"


member_axes = Table(
    "member_axes",
    Base.metadata,
    Column("member_id", ForeignKey("members.id"), primary_key=True),
    Column("axis_id", ForeignKey("axes.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.MEMBER)
    is_active: Mapped[bool] = mapped_column(default=True)

    profile: Mapped["MemberProfile"] = relationship(back_populates="user", uselist=False)


class MemberProfile(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    first_name: Mapped[str] = mapped_column(String(120))
    last_name: Mapped[str] = mapped_column(String(120))
    photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    professional_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    grade: Mapped[str | None] = mapped_column(String(120), nullable=True)
    specialty: Mapped[str | None] = mapped_column(String(120), nullable=True)
    team: Mapped[str | None] = mapped_column(String(120), nullable=True)
    short_bio: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    interests: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    links: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    orcid_id: Mapped[str | None] = mapped_column(String(32), nullable=True)

    user: Mapped[User] = relationship(back_populates="profile")
    axes: Mapped[list["Axis"]] = relationship(secondary=member_axes, back_populates="members")
