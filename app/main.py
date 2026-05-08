from database import init_db, SessionLocal
from models import Movie, Director, Writer, Genre

def start_project():
    print("Проверяем таблицы...")
    init_db()
    
    db = SessionLocal()
    
    try:
        nolan = Director(name="Кристофер Нолан")
        brother_nolan = Writer(name="Джонатан Нолан")
        sci_fi = Genre(name="Фантастика")

        inception = Movie(
            title="Начало", 
            year=2010, 
            runtime=148.0, 
            director=nolan,
            writer=brother_nolan,
            budget_count=160000000,
            gross_count=836000000
        )
        inception.genres.append(sci_fi)
        inception.rating = 8.8
        
        db.add(inception) 
        
        db.commit() 
        print("Данные теперь в базе MySQL!")
        
    except Exception as e:
        db.rollback()
        print(f"ОШИБКА: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    start_project()