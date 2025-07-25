from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey

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
    bio_min: Mapped[str] = mapped_column(nullable=True)
    bio_max: Mapped[str] = mapped_column(nullable=True)
    geo: Mapped[str] = mapped_column(nullable=True)
    icon_company: Mapped[str] = mapped_column(nullable=True)
    url_company: Mapped[str] = mapped_column(nullable=True)
    contact: Mapped[str] = mapped_column(nullable=True)
    use_technologists: Mapped[str] = mapped_column(nullable=True)
    type_company: Mapped[str] = mapped_column(nullable=True)
    number: Mapped[int] = mapped_column(nullable=True)
    off_name: Mapped[str] = mapped_column(nullable=True)
    main_people: Mapped[str] = mapped_column(nullable=True)

    # __mapper_args__ = {
    #     'polymorphic_on': type,
    #     'polymorphic_identity': 'category'
    # }


# class ImgFileModelCompany(CompanyModel):
#     __tablename__ = "ImgFile"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped [str] = mapped_column(ForeignKey("Company.name"), nullable=True)
#     type_company: Mapped[str] = mapped_column(ForeignKey("Company.type_company"), nullable=True)
#     main_people: Mapped[str] = mapped_column(ForeignKey("Company.main_people"), nullable=True)
#
#
#     __mapper_args__ = {
#         'polymorphic_identity': 'ImgFileModelCompany'
#     }
