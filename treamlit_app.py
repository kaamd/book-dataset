import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Book dataset", page_icon="📚")
st.title("📚 Book dataset")
st.write(
    """
    Это приложение показывает рейтинг японских авторов, книги которых издавались чаще других за последнии 10 лет в России
    """
)

# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\user\Downloads\japanese_books (1).csv")
    return df

df = load_data()

# Show a multiselect widget with the genres using `st.multiselect`.
genres = st.multiselect(
    "author",
    df.author.unique(),
    ["Харуки Мураками", "Содзи Симада", "Котаро Исака", "Нацухико Кёгоку", "Канаэ Минато", "Аша Лемми", "Кэйго Хигасино","Харольд Сакуиси", "Тору Фудзисава"],
)

# Filter the dataframe based on the widget input and reshape it.
df_filtered = df[(df["author"].isin(authors))]

# Prepare the data for the bar chart.
df_grouped = df_filtered.groupby(['author', 'title']).size().reset_index(name='count')

df_reshaped = df_filtered.pivot_table(
df_filtered['index'] = df_filtered.index + 1  # Создаем новый столбец с порядковым номером
df_grouped = df_filtered.groupby(['index', 'author'])['title'].apply(list).reset_index()  # Группируем по индексу и жанру

df_reshaped = df_grouped.pivot_table(
    index='index', columns='author', values='title', aggfunc=lambda x: x, fill_value=0
)
df_reshaped = df_reshaped.sort_values(by="author")

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_reshaped,
    use_container_width=True,
    column_config={"index": st.column_config.TextColumn("Number")},
)

# Display the data as an Altair chart using `st.altair_chart`.
df_chart = pd.melt(
    df_reshaped.reset_index(), id_vars="Number", var_name="author", value_name="title"
)
# Create the bar chart
chart = alt.Chart(df_grouped).mark_bar().encode(
    x=alt.X('sum(count):Q', title='Количество книг'),
    y=alt.Y('author:N', title='Авторы', sort='-x'),
    color='title:N',  # Цвет по названию книги
    tooltip=['title:N', 'count:Q']  # Информация при наведении
).properties(height=400)

# Display the data as a bar chart using `st.altair_chart`.
st.altair_chart(chart, use_container_width=True)
