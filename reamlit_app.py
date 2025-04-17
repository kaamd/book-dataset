import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Book dataset", page_icon="📚")
st.title("📚 Book dataset")
st.write(
    """
    Это приложение показывает рейтинг японских авторов, книги которых издавались чаще других за последнии 10 лет в России.
    """
)

# Load the data from a CSV.
@st.cache_data
def load_data():
    df = pd.read_csv("japanese_books (1).csv")
    return df

df = load_data()

# Получаем уникальные авторы в том порядке, в котором они находятся в DataFrame
ordered_authors = df['author'].unique()

# Show a multiselect widget with the authors using `st.multiselect`, используем ordered_authors
authors = st.multiselect(
    "Выберите авторов",
    ordered_authors,
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


# Filter the dataframe based on the selected authors.
df_filtered = df[df["author"].isin(authors)]

# Добавляем новый столбец с порядковым номером
df_filtered['index'] = df_filtered.index + 1

# С группировка по 'author' и агрегация названий книг
df_grouped = df_filtered.groupby(['index', 'author'])['title'].apply(lambda x: ', '.join(x)).reset_index()

# Сортируем только выбранные авторы по порядку появления в оригинальном DataFrame
df_grouped['author'] = pd.Categorical(df_grouped['author'], categories=ordered_authors, ordered=True)
df_grouped.sort_values('author', inplace=True)

# Переформатируем DataFrame в сводную таблицу
df_reshaped = df_grouped.pivot(index='index', columns='author', values='title').fillna('')

# Переименовываем индекс и выводим таблицу
df_reshaped.index.name = '№'

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_reshaped.style.set_table_attributes('class="streamlit-table"'),
    use_container_width=True,
)

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_reshaped,
    use_container_width=True,
)
# Prepare data for the bar chart.
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

# Display the data as a bar chart using `st.altair_chart`.
st.altair_chart(chart, use_container_width=True)
