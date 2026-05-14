from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PersonBase(BaseModel):
    name: str

class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Actor(Person): pass
class Director(Person): pass
class Writer(Person): pass

class MovieBase(BaseModel):
    title: str
    year: int
    runtime: float
    budget_count: int
    gross_count: int
    rating: float = Field(ge=0, le=10)

class MovieCreate(MovieBase):
    director_id: int
    writer_id: int
    actor_ids: List[int] = []
    genre_ids: List[int] = []

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = None
    budget_count: Optional[int] = None
    gross_count: Optional[int] = None


class Movie(MovieBase):
    id: int
    director: Director
    writer: Writer
    actors: List[Actor]
    genres: List[Genre]
    
    model_config = ConfigDict(from_attributes=True)