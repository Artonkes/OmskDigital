from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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
    name: Mapped[str]
    target: Mapped[str]
    logo: Mapped[str]
    contacts: Mapped[str]
    type_company: Mapped[str]
    quantity: Mapped[int]
