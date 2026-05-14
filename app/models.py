from typing import List, Optional
from sqlalchemy import String, Integer, Float, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

movie_actor_assoc = Table(
    "movie_actor", Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("actor_id", ForeignKey("actors.id"), primary_key=True)
)

movie_genre_assoc = Table(
    "movie_genre", Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True)
)

class Person(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

class Director(Person):
    __tablename__ = "directors"
    movies: Mapped[List["Movie"]] = relationship(back_populates="director")
    def __repr__(self): return f"Режиссер: {self.name}"

class Actor(Person):
    __tablename__ = "actors"
    movies: Mapped[List["Movie"]] = relationship(secondary=movie_actor_assoc, back_populates="actors")
    def __repr__(self): return f"Актер: {self.name}"

class Writer(Person):
    __tablename__ = "writers"
    movies: Mapped[List["Movie"]] = relationship(back_populates="writer")
    def __repr__(self): return f"Сценарист: {self.name}"

class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    movies: Mapped[List["Movie"]] = relationship(secondary=movie_genre_assoc, back_populates="genres")
    def __repr__(self): return self.name

class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    year: Mapped[int] = mapped_column(Integer)
    runtime: Mapped[float] = mapped_column(Float)
    budget_count: Mapped[int] = mapped_column(Integer) # Бюджет
    gross_count: Mapped[int] = mapped_column(Integer)  # Сборы
    _rating: Mapped[float] = mapped_column("rating", Float, default=0.0)

    director_id: Mapped[int] = mapped_column(ForeignKey("directors.id"))
    writer_id: Mapped[int] = mapped_column(ForeignKey("writers.id"))

    director: Mapped["Director"] = relationship(back_populates="movies")
    writer: Mapped["Writer"] = relationship(back_populates="movies")
    genres: Mapped[List["Genre"]] = relationship(secondary=movie_genre_assoc, back_populates="movies")
    actors: Mapped[List["Actor"]] = relationship(secondary=movie_actor_assoc, back_populates="movies")

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value: float):
        if 0 <= value <= 10:
            self._rating = value
        else:
            raise ValueError(f"Ошибка: Рейтинг {value} вне диапазона 0-10")

    def get_full_info(self):
        return (f"Фильм: '{self.title}' ({self.year})\n"
                f"Режиссер: {self.director.name if self.director else 'Неизвестен'}\n"
                f"Рейтинг: {self.rating}\n"
                f"Актёрский состав: {self.actors.name if self.actors else "Неизвестен"}\n"
                f"Бюджет: {self.budget_count}\n")