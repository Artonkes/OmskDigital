from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class CompanyModel(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    icon: Mapped[str] = mapped_column()
    bio_min: Mapped[str] = mapped_column()
    bio_max: Mapped[str] = mapped_column()
    keywords: Mapped[str] = mapped_column()
    target: Mapped[str] = mapped_column(nullable=True)
    geo: Mapped[str] = mapped_column()
    coordinates: Mapped[str] = mapped_column()
    use_technology: Mapped[str] = mapped_column()
    contact_number_phone: Mapped[str] = mapped_column()
    contact_email: Mapped[str] = mapped_column()
    contact_site: Mapped[str] = mapped_column()
    contact_tg: Mapped[str] = mapped_column()
    contact_vk: Mapped[str] = mapped_column()
    official_name: Mapped[str] = mapped_column()
    founding_data: Mapped[str] = mapped_column()
    photo_company: Mapped[str] = mapped_column(JSON, nullable=True)


class ProjectCompanyModel(Base):
    __tablename__ = "project_companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_company: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    name_project: Mapped[str] = mapped_column()
    photo: Mapped[str] = mapped_column(nullable=True)