from src.load_data import films_dict
from src.del_add_film import add_film
f=add_film()
films_dict.append(f)
print(films_dict[5421])