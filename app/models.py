class Person:
    def __init__(self, name: str):
        self.name = name

class Director(Person):
    def __repr__(self):
        return f"Режиссер: {self.name}"

class Actor(Person):
    def __repr__(self):
        return f"Актер: {self.name}"
    
class Writer(Person):
    def __repr__(self):
        return f"Актер: {self.name}"

class Genre:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name
    
class Movie:
    def __init__(self, title: str, year: int, director: Director, writer: Writer):
        self.title = title
        self.year = year
        self.director = director
        self.writer = writer

        self._rating = 0.0
        self.genres = []
        self.actors = []

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value: float):
        if 0 <= value <= 10:
            self._rating = value
        else:
            print(f"Ошибка: Рейтинг {value} не лежит в диапазоне от 0 до 10!")

    def add_genre(self, genre: Genre):
        if genre not in self.genres:
            self.genres.append(genre)

    def add_actor(self, actor: Actor):
        if actor not in self.actors:
            self.actors.append(actor)

    def get_full_info(self):
        genres_str = ", ".join([g.name for g in self.genres])
        return (f"Фильм: '{self.title}' ({self.year})\n"
                f"Режиссер: {self.director.name}\n"
                f"Сценарист: {self.writer.name}\n"
                f"Жанр: {genres_str}\n"
                f"Рейтинг: {self.rating}")

    def __repr__(self):
        return f"Movie('{self.title}')"
    
class MovieLibrary:
    def __init__(self):
        self._movies = []

    def add_movie(self, movie: Movie):
        self._movies.append(movie)
        print(f"Фильм '{movie.title}' добавлен в библиотеку.")

    def find_by_title(self, title: str):
        return [m for m in self._movies if title.lower() in m.title.lower()]

    def list_all_movies(self):
        for m in self._movies:
            print(m.get_full_info())
            print("-" * 20)

# 1. Создаем объекты людей и жанров
nolan = Director("Кристофер Нолан")
bale = Actor("Кристиан Бэйл")
sci_fi = Genre("Научная фантастика")
epstein = Writer("Джеффри Эпштейн")
drama = Genre("Драма")

# 2. Создаем фильм
interstellar = Movie("Интерстеллар", 2014, nolan, epstein)
interstellar.add_genre(sci_fi)
interstellar.add_genre(drama)
interstellar.add_actor(bale)
interstellar.rating = 8.7  # Работает сеттер

# 3. Работаем с библиотекой
library = MovieLibrary()
library.add_movie(interstellar)

# 4. Вывод данных
print("\n--- СОДЕРЖИМОЕ БИБЛИОТЕКИ ---")
library.list_all_movies()