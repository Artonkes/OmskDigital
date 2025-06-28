from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class CollegeModel(Base):
    __tablename__ = "College"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    bio: Mapped[str]
    max_ball: Mapped[int]
    min_ball: Mapped[int]
    paid_places: Mapped[int]
    free_places: Mapped[int]

class VacancyModel(Base):
    __tablename__ = "Vacancy"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    bio: Mapped[str]
    work_experience: Mapped[int]
    schedule: Mapped[str]
    work_format: Mapped[str]
    salary: Mapped[int]
    city: Mapped[str]

