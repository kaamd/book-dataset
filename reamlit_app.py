import altair as alt
import pandas as pd
import streamlit as st

# заголовок и описание страницы.
st.set_page_config(page_title="Book dataset", page_icon="📚")
st.title("📚 Book dataset")
st.write(
    """
    Это приложение показывает рейтинг японских авторов, книги которых издавались чаще других в России.
    """
)
# Загрузка данных из файла CSV.
@st.cache_data
def load_data():
    df = pd.read_csv("japanese_books.csv")
    return df
df = load_data()

# Выбор авторов с использованием уникальных значений из DataFrame
authors = st.multiselect(
    "Выберите авторов",
    options=sorted(df["author"].unique()),  # Получаем уникальные имена авторов напрямую
    default=[
        "Котаро Исака", 
        "Содзи Симада", 
        "Харуки Мураками", 
        "Нацухико Кёгоку", 
        "Канаэ Минато", 
        "Аша Лемми", 
        "Кэйго Хигасино", 
        "Харольд Сакуиси", 
        "Тору Фудзисава",
    ],
)
# Фильтрация DataFrame по выбранным авторам
if authors:
    df_filtered = df[df["author"].isin(authors)][["author", "title", "link"]].reset_index(drop=True)
# Проверка, есть ли отфильтрованные данные
    if not df_filtered.empty:
# Добавление порядкового номера
        df_filtered['№'] = range(1, len(df_filtered) + 1)
# Подсчет количества книг у каждого автора
        author_counts = df_filtered['author'].value_counts().reset_index()
        author_counts.columns = ['author', 'count']
# Объединение с отфильтрованными данными
        df_merged = df_filtered.merge(author_counts, on='author')
# Сортировка по количеству книг от большего к меньшему
        df_sorted = df_merged.sort_values(by='count', ascending=False)
# Добавление столбца "о книге" с ссылкой на книгу
        df_sorted['о книге'] = df_sorted['link'].apply(lambda x: f'<a href="{x}">Ссылка на книгу</a>')
# Именование колонок в таблице
        df_final = df_sorted[['№','author', 'title', 'о книге']]
# Отображение таблицы
    st.markdown(
    """
    <style>
    .streamlit-table {
        border-collapse: collapse;
        width: 100%;
    }
    
    .streamlit-table th, .streamlit-table td {
        max-width: 200px;
        text-align: left;
        padding: 5px;
        overflow-wrap: break-word;
        word-wrap: break-word;
        word-break: break-word;
        white-space: normal;
        border: 1px solid #ddd;
    }
    
    .streamlit-table th {
        background-color: #D0E9C6; /* Обновленный светло-зеленый цвет фона */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Отображаем таблицу
        st.dataframe(
            df_final.style.set_table_attributes('class="streamlit-table"'),
            use_container_width=True,
        )
# Получение уникальных авторов в порядке, которые мы использовали в таблице
        unique_authors_order = df_final['author'].tolist()
# Подготвка данных для столбчатой диаграммы
        df_chart = df_filtered.groupby(['author', 'title']).size().reset_index(name='count')
# Проверяем, что count является целым числом
        chart = alt.Chart(df_chart).mark_bar().encode(
        x=alt.X('sum(count):Q', title='Количество книг', axis=alt.Axis(format='d', ticks=True, grid=False)),  # Форматируем ось X как целое число
        y=alt.Y('author:N', title='Авторы', sort=unique_authors_order),  # Применяем порядок из списка,
        color='title:N',  # Цвет по названию книги
        tooltip=['title:N', 'count:Q']  # Информация при наведении
        ).properties(height=400)    
# Убедитесь, что на оси X отображаются только уникальные значения
        chart = chart.encode(
        x=alt.X('sum(count):Q', title='Количество книг', axis=alt.Axis(format='d', ticks=True, grid=False, values=[0, 1, 2, 3, 4, 5]))  # Указать значения, которые хотим видеть на оси X
        )
# Отображаем данные в виде столбчатой диаграммы
        st.altair_chart(chart, use_container_width=True)
else:
        st.write("Нет данных. Необходимо выбрать авторов из списка.")
