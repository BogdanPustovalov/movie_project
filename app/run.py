import streamlit as st
from database import SessionLocal, engine, Base
from services import MovieService, PersonService, GenreService
from repositories import DirectorRepository, ActorRepository, GenreRepository, WriterRepository
from schemas import MovieCreate

st.set_page_config(page_title="Movie DB Management", layout="wide")

Base.metadata.create_all(bind=engine)
db = SessionLocal()
movie_service = MovieService(db)
genre_service = GenreService(db)

dir_repo = DirectorRepository(db)
actor_repo = ActorRepository(db)
genre_repo = GenreRepository(db)
writer_repo = WriterRepository(db)

st.title("Система управления базой фильмов")

menu = ["Список фильмов", "Добавить фильм", "Аналитика"]
choice = st.sidebar.selectbox("Меню", menu)


actor_service = PersonService(db, ActorRepository(db))
director_service = PersonService(db, DirectorRepository(db))
writer_service = PersonService(db, WriterRepository(db))

st.sidebar.markdown("---")
st.sidebar.header("Быстрое добавление")

with st.sidebar.expander("Добавить персону"):
    p_type = st.selectbox("Кто это?", ["Актер", "Режиссер", "Сценарист"])
    p_name = st.text_input("Имя и фамилия")
    if st.button("Добавить"):
        if p_name:
            if p_type == "Актер":
                actor_service.add_person(p_name)
            elif p_type == "Режиссер":
                director_service.add_person(p_name)
            else:
                writer_service.add_person(p_name)
            st.success(f"{p_type} добавлен!")
            st.rerun()

with st.sidebar.expander("Добавить жанр"):
    g_name = st.text_input("Название жанра")
    if st.button("Сохранить жанр"):
        from models import Genre
        new_g = Genre(name=g_name)
        db.add(new_g)
        db.commit()
        st.success("Жанр добавлен")
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("Удаление из базы")

with st.sidebar.expander("Удалить персону/жанр"):
    delete_type = st.selectbox("Что удаляем?", ["Актер", "Режиссер", "Сценарист", "Жанр"])
    
    if delete_type == "Актер":
        items = actor_repo.get_all()
    elif delete_type == "Режиссер":
        items = dir_repo.get_all()
    elif delete_type == "Сценарист":
        items = writer_repo.get_all()
    else:
        items = genre_repo.get_all()

    target = st.selectbox("Выберите объект", options=items, format_func=lambda x: x.name)
    
    confirm_delete = st.button("❌ Удалить навсегда", type="primary")

    if confirm_delete and target:
        try:
            if delete_type == "Актер":
                actor_service.delete_person(target.id)
            elif delete_type == "Режиссер":
                director_service.delete_person(target.id)
            elif delete_type == "Сценарист":
                writer_service.delete_person(target.id)
            elif delete_type == "Жанр":
                genre_service.delete_genre(target.id)
            
            st.success(f"Удалено: {target.name}")
            st.rerun()
        except ValueError as e:
            st.error(str(e))

if choice == "Список фильмов":
    st.header("Список и поиск фильмов")

    with st.container():
        st.subheader("Фильтры и сортировка")
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        
        with col1:
            search_title = st.text_input("Название")
        
        with col2:
            all_genres = genre_service.get_all_genres()
            genre_options = [None] + all_genres
            selected_genre = st.selectbox(
                "Жанр", 
                options=genre_options, 
                format_func=lambda x: x.name if x else "Все"
            )
            
        with col3:
            sort_field = st.selectbox(
                "Сортировать по", 
                options=["Год", "Рейтинг", "Бюджет", "Сборы", "Длительность"]
            )
            
        with col4:
            order = st.selectbox("Порядок", options=["Убывание", "Возрастание"])
            is_reverse = True if order == "Убывание" else False

    st.divider()

    genre_id = selected_genre.id if selected_genre else None
    movies = movie_service.search_movies(
        title=search_title, 
        genre_id=genre_id, 
        sort_by=sort_field, 
        reverse=is_reverse
    )

    if not movies:
        st.warning("Фильмы не найдены по вашему запросу.")
    else:
        st.write(f"Найдено фильмов: {len(movies)}")
        
        for m in movies:
            with st.expander(f"🎬 {m.title} ({m.year}) — ⭐ {m.rating}"):
                
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.write(f"**Режиссер:** {m.director.name if m.director else 'Не указан'}")
                    st.write(f"**Сценарист:** {m.writer.name if m.writer else 'Не указан'}")
                    st.write(f"**Длительность:** {m.runtime} мин.")
                with col_info2:
                    st.write(f"**Бюджет:** ${m.budget_count:,}")
                    st.write(f"**Сборы:** ${m.gross_count:,}")
                    st.write(f"**Жанры:** {', '.join([g.name for g in m.genres])}")
                
                st.write(f"**Актеры:** {', '.join([a.name for a in m.actors])}")
                
                st.divider()

                if st.checkbox(f"📝 Редактировать данные", key=f"edit_check_{m.id}"):
                    with st.form(key=f"edit_form_{m.id}"):
                        edit_title = st.text_input("Название", value=m.title)
                        
                        ec1, ec2, ec3 = st.columns(3)
                        with ec1:
                            edit_year = st.number_input("Год", value=m.year)
                        with ec2:
                            edit_runtime = st.number_input("Длительность", value=m.runtime)
                        with ec3:
                            edit_rating = st.number_input("Рейтинг", value=m.rating, min_value=0.0, max_value=10.0)
                        
                        edit_budget = st.number_input("Бюджет", value=m.budget_count)
                        edit_gross = st.number_input("Сборы", value=m.gross_count)
                        
                        all_dirs = dir_repo.get_all()
                        dir_index = 0
                        try:
                            dir_index = next(i for i, d in enumerate(all_dirs) if d.id == m.director_id)
                        except StopIteration: dir_index = 0

                        new_dir = st.selectbox("Режиссер", options=all_dirs, index=dir_index, format_func=lambda x: x.name)
                        
                        all_actors = actor_repo.get_all()
                        current_actor_ids = [a.id for a in m.actors]
                        new_actors = st.multiselect("Актеры", options=all_actors, 
                                                    default=[a for a in all_actors if a.id in current_actor_ids],
                                                    format_func=lambda x: x.name)
                        
                        all_genres = genre_service.get_all_genres()
                        current_genre_ids = [g.id for g in m.genres]
                        new_genres = st.multiselect("Жанры", options=all_genres, 
                                                     default=[g for g in all_genres if g.id in current_genre_ids],
                                                     format_func=lambda x: x.name)

                        if st.form_submit_button("💾 Сохранить изменения"):
                            try:
                                updated_data = MovieCreate(
                                    title=edit_title, year=edit_year, runtime=edit_runtime,
                                    budget_count=edit_budget, gross_count=edit_gross,
                                    rating=edit_rating, director_id=new_dir.id,
                                    writer_id=m.writer_id,
                                    actor_ids=[a.id for a in new_actors],
                                    genre_ids=[g.id for g in new_genres]
                                )
                                movie_service.update_movie(m.id, updated_data)
                                st.success("Данные обновлены!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Ошибка: {e}")

                if st.button(f"🗑 Удалить фильм", key=f"del_btn_{m.id}", type="secondary"):
                    movie_service.delete_movie(m.id)
                    st.success("Фильм удален")
                    st.rerun()

elif choice == "Добавить фильм":
    st.header("Добавление нового фильма")
    
    with st.form("movie_form"):
        title = st.text_input("Название фильма")
        col1, col2, col3 = st.columns(3)
        with col1:
            year = st.number_input("Год", min_value=1895, max_value=2030, value=2023)
        with col2:
            runtime = st.number_input("Длительность (мин)", min_value=1.0, value=120.0)
        with col3:
            rating = st.slider("Рейтинг", 0.0, 10.0, 5.0)
            
        col4, col5 = st.columns(2)
        with col4:
            budget = st.number_input("Бюджет ($)", min_value=0, value=1000000)
        with col5:
            gross = st.number_input("Сборы ($)", min_value=0, value=2000000)

        directors = dir_repo.get_all()
        writers = writer_repo.get_all()
        actors_list = actor_repo.get_all()
        genres_list = genre_repo.get_all()

        director = st.selectbox("Режиссер", options=directors, format_func=lambda x: x.name)
        writer = st.selectbox("Сценарист", options=writers, format_func=lambda x: x.name)
        
        selected_actors = st.multiselect("Актеры", options=actors_list, format_func=lambda x: x.name)
        selected_genres = st.multiselect("Жанры", options=genres_list, format_func=lambda x: x.name)

        submit = st.form_submit_button("Сохранить фильм")

        if submit:
            try:
                new_movie_data = MovieCreate(
                    title=title,
                    year=year,
                    runtime=runtime,
                    budget_count=budget,
                    gross_count=gross,
                    rating=rating,
                    director_id=director.id,
                    writer_id=writer.id,
                    actor_ids=[a.id for a in selected_actors],
                    genre_ids=[g.id for g in selected_genres]
                )
                movie_service.create_new_movie(new_movie_data)
                st.success(f"Фильм '{title}' успешно добавлен!")
            except Exception as e:
                st.error(f"Ошибка при сохранении: {e}")

elif choice == "Аналитика":
    st.header("Анализ данных")
    movies = movie_service.get_all_movies()
    if movies:
        import pandas as pd
        data = [
            {"Title": m.title, "Budget": m.budget_count, "Gross": m.gross_count, "Rating": m.rating}
            for m in movies
        ]
        df = pd.DataFrame(data)
        
        st.subheader("Бюджет vs Сборы")
        st.scatter_chart(df, x="Budget", y="Gross", color="Title")
        
        st.subheader("Топ-фильмов по рейтингу")
        st.bar_chart(df.set_index("Title")["Rating"])
    else:
        st.write("Нет данных для анализа")

db.close()