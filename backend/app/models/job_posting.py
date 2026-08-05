import enum
from datetime import datetime

from sqlalchemy import String, Text, Integer, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PostingStatus(str, enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class JobPosting(Base):
    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    job_category: Mapped[str] = mapped_column(String(100), nullable=True)
    employment_type: Mapped[str] = mapped_column(String(50), nullable=True)
    career_level: Mapped[str] = mapped_column(String(50), nullable=True)
    career_years_min: Mapped[int] = mapped_column(Integer, nullable=True)
    career_years_max: Mapped[int] = mapped_column(Integer, nullable=True)
    location: Mapped[str] = mapped_column(String(200), nullable=True)
    salary_type: Mapped[str] = mapped_column(String(50), nullable=True)
    salary_min: Mapped[int] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int] = mapped_column(Integer, nullable=True)
    required_skills: Mapped[str] = mapped_column(Text, nullable=True)  # 콤마 구분 문자열
    description: Mapped[str] = mapped_column(Text, nullable=True)
    qualifications: Mapped[str] = mapped_column(Text, nullable=True)
    preferred_qualifications: Mapped[str] = mapped_column(Text, nullable=True)
    benefits: Mapped[str] = mapped_column(Text, nullable=True)
    apply_start_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    apply_end_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[PostingStatus] = mapped_column(
        Enum(PostingStatus), default=PostingStatus.OPEN, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), server_default=func.now()
    )

    company: Mapped["Company"] = relationship("Company", lazy="joined")
