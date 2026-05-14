from sqlalchemy.orm import Session
from sqlalchemy import select, desc, asc
import models, schemas

class BaseRepository:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def get_by_id(self, obj_id: int):
        return self.db.query(self.model).filter(self.model.id == obj_id).first()

    def get_all(self):
        return self.db.query(self.model).all()
    
    def create(self, **kwargs):
        obj = self.model(**kwargs)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def delete(self, obj):
        self.db.delete(obj)
        self.db.commit()

class MovieRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, models.Movie)

    def get_by_title(self, title: str):
        return self.db.query(models.Movie).filter(models.Movie.title == title).first()

    def create(self, movie_data: schemas.MovieCreate, actors: list, genres: list):
        db_movie = models.Movie(
            title=movie_data.title,
            year=movie_data.year,
            runtime=movie_data.runtime,
            budget_count=movie_data.budget_count,
            gross_count=movie_data.gross_count,
            rating=movie_data.rating,
            director_id=movie_data.director_id,
            writer_id=movie_data.writer_id
        )
        db_movie.actors = actors
        db_movie.genres = genres
        
        self.db.add(db_movie)
        self.db.commit()
        self.db.refresh(db_movie)
        return db_movie
    
    def search(self, title: str = None, genre_id: int = None, sort_by: str = "year", reverse: bool = True):
        query = self.db.query(models.Movie)
        
        if title:
            query = query.filter(models.Movie.title.ilike(f"%{title}%"))
        if genre_id:
            query = query.join(models.Movie.genres).filter(models.Genre.id == genre_id)
        
        sort_map = {
            "Рейтинг": models.Movie._rating,
            "Год": models.Movie.year,
            "Бюджет": models.Movie.budget_count,
            "Сборы": models.Movie.gross_count,
            "Длительность": models.Movie.runtime
        }
        
        column = sort_map.get(sort_by, models.Movie.year)
        
        if reverse:
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))
            
        return query.all()
    
    def update(self, movie_obj, actors, genres, **kwargs):
        for key, value in kwargs.items():
            setattr(movie_obj, key, value)
        
        movie_obj.actors = actors
        movie_obj.genres = genres
        
        self.db.commit()
        self.db.refresh(movie_obj)
        return movie_obj
    
class ActorRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, models.Actor)

    def get_many(self, actor_ids: list[int]):
        return self.db.query(models.Actor).filter(models.Actor.id.in_(actor_ids)).all()

class GenreRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, models.Genre)

    def get_many(self, genre_ids: list[int]):
        return self.db.query(models.Genre).filter(models.Genre.id.in_(genre_ids)).all()

class DirectorRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, models.Director)

class WriterRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, models.Writer)