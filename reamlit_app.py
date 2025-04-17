import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Book dataset", page_icon="📚")
st.title("📚 Book dataset")
st.write(
    """
    Это приложение показывает рейтинг японских авторов, книги которых издавались чаще других за последние 10 лет в России.
    """
)

# Load the data from a CSV.
@st.cache_data
def load_data():
    df = pd.read_csv("japanese_books (1).csv")
    return df

df = load_data()

# Отображение всех авторов и названий книг без выбора
df_filtered = df[["author", "title", "link"]].reset_index(drop=True)

# Создание новой колонки для отображения ссылок с гиперссылками
df_filtered['link'] = df_filtered['link'].apply(lambda x: f'<a href="{x}">Ссылка на книгу</a>')

# Переформатирование DataFrame в сводную таблицу
df_reshaped = df_filtered.pivot(columns='author', values='link').fillna('')

# Переименование индекса и добавление нумерации
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

# Подготовка данных для диаграммы.
df_chart = df_filtered.groupby(['author', 'title']).size().reset_index(name='count')

# Предполагаем, что count является целым числом
chart = alt.Chart(df_chart).mark_bar().encode(
    x=alt.X('sum(count):Q', title='Количество книг', axis=alt.Axis(format='d', ticks=True, grid=False)),  # Форматируем ось X как целое число
    y=alt.Y('author:N', title='Авторы', sort='-x'),
    color='title:N',  # Цвет по названию книги
    tooltip=['title:N', 'count:Q']  # Информация при наведении
).properties(height=400)

# Убедимся, что на оси X отображаются только уникальные значения
chart = chart.encode(
    x=alt.X('sum(count):Q', title='Количество книг', axis=alt.Axis(format='d', ticks=True, grid=False, values=[0, 1, 2, 3, 4, 5]))  # Указать значения, которые хотим видеть на оси X
)

# Отображение данных в виде столбиковой диаграммы с помощью `st.altair_chart`.
st.altair_chart(chart, use_container_width=True)
