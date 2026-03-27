from pydantic import BaseModel, EmailStr


class MemberOut(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    professional_email: str | None = None
    grade: str | None = None
    specialty: str | None = None
    team: str | None = None
    short_bio: str | None = None
    interests: str | None = None
    links: str | None = None
    orcid_id: str | None = None

    class Config:
        from_attributes = True


class MemberUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    professional_email: EmailStr | None = None
    grade: str | None = None
    specialty: str | None = None
    team: str | None = None
    short_bio: str | None = None
    interests: str | None = None
    links: str | None = None
    orcid_id: str | None = None
