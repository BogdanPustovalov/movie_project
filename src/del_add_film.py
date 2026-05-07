from src.load_data import films_dict

def add_film():
    name_film=str(input(('Введите название фильма: ')))
    genre=str(input(('Введите жанр: ')))
    year=int(input(('Введите год: ')))
    score=float(input(('Введите оценку фильма: ')))
    director=str(input(('Введите режиссёра фильма: ')))
    writer=str(input(('Введите сценариста фильма: ')))
    star=str(input('Введите актёра, исполнившего главную роль: '))
    country=str(input('Введите страну, где снят фильм: '))
    budget=float(input('Введите бюджет фильма: '))
    gross=float(input('Введите кассовые сборы фильма: '))
    company=str(input('Введите компанию, снявшую фильм: '))
    time=float(input('Введите длительность фильма: '))
    film={
        "film": name_film,
        "genre": genre,
        "year": year,
        "score": score,
        "director": director,
        "writer": writer,
        "star": star,
        "country": country,
        "budget": budget,
        "gross": gross,
        "company": company,
        "runtime": time,
    }
    return film