from datetime import date

from pydantic import BaseModel


class AxisIn(BaseModel):
    title: str
    description: str | None = None
    manager_name: str | None = None


class AxisOut(AxisIn):
    id: int

    class Config:
        from_attributes = True


class PublicationIn(BaseModel):
    axis_id: int | None = None
    title: str
    authors: str
    publication_type: str
    year: int
    venue: str | None = None
    abstract: str | None = None
    keywords: str | None = None
    doi: str | None = None
    external_link: str | None = None
    pdf_link: str | None = None


class PublicationOut(PublicationIn):
    id: int
    owner_id: int
    status: str

    class Config:
        from_attributes = True


class CommunicationIn(BaseModel):
    title: str
    authors: str
    event_name: str
    communication_type: str
    location: str | None = None
    country: str | None = None
    event_date: date | None = None
    abstract: str | None = None
    communication_status: str = "submitted"
    document_link: str | None = None


class CommunicationOut(CommunicationIn):
    id: int
    owner_id: int
    validation_status: str

    class Config:
        from_attributes = True


class EventIn(BaseModel):
    axis_id: int | None = None
    title: str
    description: str | None = None
    place: str | None = None
    event_date: date | None = None
    speakers: str | None = None
    poster_url: str | None = None
    status: str = "upcoming"


class EventOut(EventIn):
    id: int

    class Config:
        from_attributes = True


class NewsIn(BaseModel):
    title: str
    content: str
    is_published: bool = False


class NewsOut(NewsIn):
    id: int

    class Config:
        from_attributes = True


class ProjectIn(BaseModel):
    axis_id: int | None = None
    title: str
    summary: str | None = None
    manager: str | None = None
    partners: str | None = None
    funding: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = None


class ProjectOut(ProjectIn):
    id: int

    class Config:
        from_attributes = True


class ContactMessageIn(BaseModel):
    full_name: str
    email: str
    subject: str
    message: str


class ContactMessageOut(ContactMessageIn):
    id: int
    is_processed: bool

    class Config:
        from_attributes = True


class DocumentOut(BaseModel):
    id: int
    owner_id: int
    publication_id: int | None = None
    communication_id: int | None = None
    original_name: str
    stored_name: str
    storage_backend: str
    file_url: str
    mime_type: str | None = None
    size_bytes: int

    class Config:
        from_attributes = True


class ValidationOut(BaseModel):
    id: int
    content_type: str
    content_id: int
    previous_status: str | None = None
    new_status: str
    note: str | None = None
    validator_user_id: int

    class Config:
        from_attributes = True
