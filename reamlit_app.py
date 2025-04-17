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

# Show a multiselect widget with the authors using `st.multiselect`.
authors = st.multiselect(
    "Выберите авторов",
    df.author.unique(),
    ["Харуки Мураками", "Содзи Симада", "Котаро Исака", "Нацухико Кёгоку", "Канаэ Минато", "Аша Лемми", "Кэйго Хигасино", "Харольд Сакуиси", "Тору Фудзисава"],
)

# Filter the dataframe based on the selected authors.
df_filtered = df[df["author"].isin(authors)]

# Assign a sequential index to each row for display.
df_filtered['index'] = df_filtered.index + 1  # Создаем новый столбец с порядковым номером

# Group by 'author' and aggregate book titles
df_grouped = df_filtered.groupby(['index', 'author'])['title'].apply(lambda x: ', '.join(x)).reset_index()

# Reshape the dataframe to a pivot table with authors as columns
df_reshaped = df_grouped.pivot(index='index', columns='author', values='title').fillna('')

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_reshaped,
    use_container_width=True,
)

# Prepare data for the bar chart.
df_chart = df_filtered.groupby(['author', 'title']).size().reset_index(name='count')

# Create the bar chart
chart = alt.Chart(df_chart).mark_bar().encode(
x=alt.X('sum(count):Q', title='Количество книг'),
y=alt.Y('author:N', title='Авторы', sort='-x'),
color='title:N',  # Цвет по названию книги
tooltip=['title:N', 'count:Q']  # Информация при наведении
).properties(height=400)

# Display the data as a bar chart using `st.altair_chart`.
st.altair_chart(chart, use_container_width=True)
