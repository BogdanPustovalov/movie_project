from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Настройки подключения (замени на свои данные)
DB_URL = "mysql+pymysql://root:EfNj4u9b2r9Wjck@localhost/movie_db"

class Base(DeclarativeBase):
    pass

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    # Эта команда создаст все таблицы в MySQL
    Base.metadata.create_all(bind=engine)