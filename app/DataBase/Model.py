from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


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
    contact_tg: Mapped[str] = mapped_column(nullable=True)
    contact_vk: Mapped[str] = mapped_column(nullable=True)
    official_name: Mapped[str] = mapped_column(nullable=True)
    founding_data: Mapped[str] = mapped_column(nullable=True)
    photo_company: Mapped[str] = mapped_column(JSON, nullable=True)


class ProjectCompanyModel(Base):
    __tablename__ = "ProjectCompany"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_company: Mapped[int] = mapped_column()
    name_company: Mapped[str] = mapped_column()
    name_project: Mapped[str] = mapped_column()
    photo: Mapped[str] = mapped_column()
