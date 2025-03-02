from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str | None] = mapped_column(nullable=True)
    tags: Mapped[str | None] = mapped_column(nullable=True)
    difficulty: Mapped[str | None] = mapped_column(nullable=True)
    instructor_name: Mapped[str | None] = mapped_column(nullable=True)
    url: Mapped[str] = mapped_column(unique=True, nullable=False)
    summary: Mapped[str | None] = mapped_column(nullable=True)
    description: Mapped[str | None] = mapped_column(nullable=True)
    reviews: Mapped[int] = mapped_column(default=0)
    duration: Mapped[str] = mapped_column(default="0")
    enrolled: Mapped[int] = mapped_column(default=0)
    rating: Mapped[float] = mapped_column(default=0.0)
    language: Mapped[str | None] = mapped_column(nullable=True)
    price: Mapped[str | None] = mapped_column(nullable=True)
    image_url: Mapped[str | None] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"Course(id={self.id}, name={self.name}, url={self.url})"
