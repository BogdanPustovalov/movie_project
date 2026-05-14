import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

current_file_path = Path(__file__).resolve()
BASE_DIR = current_file_path.parent.parent
env_path = BASE_DIR / ".env"

if env_path.exists():
    load_dotenv(env_path)
else:
    print(f"--- ОШИБКА: Файл .env НЕ НАЙДЕН по пути: {env_path} ---")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_HOST, DB_NAME]):
    print(f"DEBUG: {DB_USER=}, {DB_HOST=}, {DB_NAME=}")
    raise ValueError(f"Не удалось загрузить данные из .env! Проверь, что файл существует здесь: {env_path}")

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

class Base(DeclarativeBase):
    pass

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)