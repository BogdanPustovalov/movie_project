from sqlalchemy.orm import Session
from repositories import MovieRepository, ActorRepository, GenreRepository, DirectorRepository, WriterRepository
import schemas
import models

class PersonService:
    def __init__(self, db: Session, repo):
        self.db = db
        self.repo = repo

    def add_person(self, name: str):
        if not name:
            raise ValueError("Имя не может быть пустым")
        return self.repo.create(name=name)

    def delete_person(self, person_id: int):
        person = self.repo.get_by_id(person_id)
        if not person:
            raise ValueError("Запись не найдена")
        
        if len(person.movies) > 0:
            raise ValueError(f"Нельзя удалить '{person.name}', так как есть фильмы с его участием!")
        
        self.repo.delete(person)

class GenreService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = GenreRepository(db)

    def get_all_genres(self):
        return self.repo.get_all()

    def add_genre(self, name: str):
        existing = self.db.query(models.Genre).filter_by(name=name).first()
        if existing:
            return existing
        return self.repo.create(name=name)
    
    def delete_genre(self, genre_id: int):
        genre = self.repo.get_by_id(genre_id)
        if not genre:
            raise ValueError("Жанр не найден")
        
        if len(genre.movies) > 0:
            raise ValueError("Нельзя удалить жанр, в котором есть фильмы!")
        
        self.repo.delete(genre)

class MovieService:
    def __init__(self, db: Session):
        self.movie_repo = MovieRepository(db)
        self.actor_repo = ActorRepository(db)
        self.genre_repo = GenreRepository(db)
        self.director_repo = DirectorRepository(db)
        self.writer_repo = WriterRepository(db)

    def create_new_movie(self, movie_data: schemas.MovieCreate):
        actors = self.actor_repo.get_many(movie_data.actor_ids)
        genres = self.genre_repo.get_many(movie_data.genre_ids)

        if not self.director_repo.get_by_id(movie_data.director_id):
            raise ValueError("Режиссер не найден")

        return self.movie_repo.create(movie_data, actors, genres)

    def get_all_movies(self):
        return self.movie_repo.get_all()

    def get_movie(self, movie_id: int):
        return self.movie_repo.get_by_id(movie_id)
    
    def delete_movie(self, movie_id: int):
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise ValueError("Фильм не найден")
        
        self.movie_repo.delete(movie)

    def search_movies(self, title: str = None, genre_id: int = None, sort_by: str = "Год", reverse: bool = True):
        return self.movie_repo.search(title, genre_id, sort_by, reverse)
    
    def update_movie(self, movie_id: int, movie_data: schemas.MovieCreate):
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise ValueError("Фильм не найден")
        
        actors = self.actor_repo.get_many(movie_data.actor_ids)
        genres = self.genre_repo.get_many(movie_data.genre_ids)
        
        update_data = movie_data.model_dump(exclude={'actor_ids', 'genre_ids'})
        
        return self.movie_repo.update(movie, actors, genres, **update_data)