import enum
from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, Enum, DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ApplicationStatus(str, enum.Enum):
    SUBMITTED = "SUBMITTED"


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    job_posting_id: Mapped[int] = mapped_column(ForeignKey("job_postings.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    applicant_name: Mapped[str] = mapped_column(String(100), nullable=False)
    applicant_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    applicant_email: Mapped[str] = mapped_column(String(255), nullable=False)
    cover_letter: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus), default=ApplicationStatus.SUBMITTED, nullable=False
    )
    applied_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint("job_posting_id", "user_id", name="uq_application_posting_user"),
    )
