import altair as alt
import pandas as pd
import streamlit as st

# заголовок и описание страницы..
st.set_page_config(page_title="Book dataset", page_icon="📚")
st.title("📚 Book dataset")
st.write(
    """ Это приложение показывает рейтинг японских авторов, книги которых издавались чаще других за последнии 10 лет в России. """)

# Загрузка данных из файла CSV.
@st.cache_data
def load_data():
    df = pd.read_csv("japanese_books (1).csv")
    return df
    
df = load_data()
# Выбор авторов с использованием уникальных значений из DataFrame
authors = st.multiselect(
    "Выберите авторов",
    options=sorted(df["author"].unique()),  # Получаем уникальные имена авторов напрямую
    default=[
        "Харуки Мураками", 
        "Содзи Симада", 
        "Котаро Исака", 
        "Нацухико Кёгоку", 
        "Канаэ Минато", 
        "Аша Лемми", 
        "Кэйго Хигасино", 
        "Харольд Сакуиси", 
        "Тору Фудзисава",
    ],
)

# Фильтрация DataFrame по выбранным авторам и выбор только необходимых колонок
df_filtered = df[df["author"].isin(authors)][["author", "title"]].reset_index(drop=True)

# Подсчет количества книг у каждого автора
author_counts = df_filtered['author'].value_counts()

# Переформатирование DataFrame в сводную таблицу
df_reshaped = df_filtered.pivot(columns='author', values='title').fillna('')

# Переупорядочиваем столбцы в сводной таблице согласно количеству книг
sorted_authors = author_counts.index.tolist()  # Получаем список авторов от большего к меньшему
df_reshaped = df_reshaped.reindex(columns=sorted_authors)

# Переименование индекса и добавление нумерации, независимой от авторов
df_reshaped.index = range(1, len(df_reshaped) + 1) 

# Настройка стиля таблицы
st.markdown(
    """
    <style>
    .streamlit-table {
        border-collapse: collapse;
        width: 100%;
    }
    .streamlit-table th, .streamlit-table td {
        max-width: 200px; /* Максимальная ширина ячеек */
        text-align: left; /* Выравнивание текста */
        padding: 5px; /* Отступы внутри ячеек */
        overflow-wrap: break-word; /* Перенос слов */
        word-wrap: break-word; /* Поддержка переноса для старых браузеров */
        word-break: break-word; /* Перенос текста на новую строку */
        white-space: normal; /* Позволяет переносить текст */
        border: 1px solid #ddd; /* Граница ячеек */
    }
    .streamlit-table th {
        background-color: #f0f0f0; /* Цвет фона заголовков */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Отображение таблицы
st.dataframe(
    df_reshaped.style.set_table_attributes('class="streamlit-table"'),
    use_container_width=True,
)

# Подготовка данных для столбчатой диаграммы.
df_chart = df_filtered.groupby(['author', 'title']).size().reset_index(name='count')

# Настройка диаграммы
chart = alt.Chart(df_chart).mark_bar().encode(
    x=alt.X('sum(count):Q', title='Количество книг', axis=alt.Axis(format='d', ticks=True, grid=False)),  # Форматируем ось X как целое число
    y=alt.Y('author:N', title='Авторы', sort='-x'),
    color='title:N',  # Цвет по названию книги
    tooltip=['title:N', 'count:Q']  # Информация при наведении
).properties(height=400)

# Проверка, что на оси X отображаются только уникальные значения
chart = chart.encode(
    x=alt.X('sum(count):Q', title='Количество книг', axis=alt.Axis(format='d', ticks=True, grid=False, values=[0, 1, 2, 3, 4, 5])) 
)
# Display the data as a bar chart using `st.altair_chart`.
st.altair_chart(chart, use_container_width=True) 
