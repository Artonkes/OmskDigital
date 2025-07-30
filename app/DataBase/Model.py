from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey, JSON
from typing import List

class Base(DeclarativeBase):
    pass

class CollegeModel(Base):
    __tablename__ = "College"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    bio: Mapped[str]
    training_time: Mapped[int]
    directions: Mapped[str]

class VacancyModel(Base):
    __tablename__ = "Vacancy"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    bio: Mapped[str]
    city: Mapped[str]
    salary: Mapped[int]
    company_name: Mapped[str]

class CompanyModel(Base):
    __tablename__ = "Company"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=True)
    icon: Mapped[str] = mapped_column(nullable=True)
    bio_min: Mapped[str] = mapped_column(nullable=True)
    bio_max: Mapped[str] = mapped_column(nullable=True)
    keywords: Mapped[str] = mapped_column(nullable=True)
    target: Mapped[str] = mapped_column(nullable=True)
    geo: Mapped[str] = mapped_column(nullable=True)
    use_technology: Mapped[str] = mapped_column(nullable=True)
    contact: Mapped[str] = mapped_column(nullable=True)
    official_name: Mapped[str] = mapped_column(nullable=True)
    founding_data: Mapped[str] = mapped_column(nullable=True)
    project: Mapped[str] = mapped_column(nullable=True)
    project_photo: Mapped[str] = mapped_column(nullable=True)
    photo_company: Mapped[str] = mapped_column(nullable=True)