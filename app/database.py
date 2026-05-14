import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 1. Определяем путь к папке, где лежит этот файл (app/)
current_file_path = Path(__file__).resolve()
# 2. Определяем корень проекта (на один уровень выше папки app)
BASE_DIR = current_file_path.parent.parent
# 3. Формируем полный путь к .env
env_path = BASE_DIR / ".env"

# --- ОТЛАДОЧНАЯ ИНФОРМАЦИЯ ---
# Если переменные не загрузятся, мы увидим это в консоли
if env_path.exists():
    load_dotenv(env_path)
    # print(f"--- .env найден и загружен из: {env_path} ---")
else:
    print(f"--- ОШИБКА: Файл .env НЕ НАЙДЕН по пути: {env_path} ---")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Если хоть одна переменная пустая - останавливаем программу с подсказкой
if not all([DB_USER, DB_HOST, DB_NAME]):
    print(f"DEBUG: {DB_USER=}, {DB_HOST=}, {DB_NAME=}") # Это покажет, что именно None
    raise ValueError(f"Не удалось загрузить данные из .env! Проверь, что файл существует здесь: {env_path}")

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

class Base(DeclarativeBase):
    pass

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)