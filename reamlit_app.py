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

    # Добавление порядкового номера
    df_filtered['№'] = range(1, len(df_filtered) + 1)
    df.index += 1  # Начинаем индексацию с 1

    # Подсчет количества книг у каждого автора
    author_counts = df_filtered['author'].value_counts().reset_index()
    author_counts.columns = ['author', 'count']

    # Объединение с отфильтрованными данными
    df_merged = df_filtered.merge(author_counts, on='author')

    # Сортировка по количеству книг от большего к меньшему
    df_sorted = df_merged.sort_values(by='count', ascending=False)

    # Удаление лишнего столбца 'count'
    df_sorted = df_sorted.drop(columns=['count'])

    # Добавление столбца "о книге" с ссылкой на книгу
    df_sorted['о книге'] = df_sorted['link'].apply(lambda x: f'<a href="{x}">Ссылка на книгу</a>')

    # Именование колонок в таблице
    df_final = df_sorted[['№', 'author', 'title', 'о книге']]

    # Настройка стиля таблицы
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
            background-color: #f0f0f0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Отображение таблицы
st.dataframe(
    df.style.set_table_attributes('class="streamlit-table"'),
    use_container_width=True,
)
# Create the bar chart
chart = alt.Chart(df_chart).mark_bar().encode(
    x=alt.X('sum(count):Q', title='Количество книг', 
             bin=alt.Bin(step=1, maxbins=100),  # Устанавливаем шаг оси X равным 1
             scale=alt.Scale(domain=[0, None])),  # Устанавливаем минимальное значение на оси X равным 0
    y=alt.Y('author:N', title='Авторы', sort='-x'),
    color='title:N',  # Цвет по названию книги
    tooltip=['title:N', 'count:Q']  # Информация при наведении
).properties(height=400)

# Display the data as a bar chart using `st.altair_chart`.
st.altair_chart(chart, use_container_width=True)
