import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt

# Main page content
st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")

st.write("This is the main page of the app.")

# load and parse the html
with open("breeds-a-to-z.html") as fp:
    soup = BeautifulSoup(fp, "html.parser") # html.parser is default

# get all the breed cards
data = soup.find_all("div", class_="m-breed-card")

# parse all the breed cards into a dataframe
breed_cards = []

for card in data:
    breed_card = dict()
    breed_card["category"] = card.find("div", class_="m-breed-card__category").string
    breed_card["name"] = card.find("strong", class_="m-breed-card__title").string
    summary = card.find("div", class_="m-breed-card__summary")
    for item in summary.find_all("div", class_="m-breed-summary__item"):
        key = item.find("span", class_="m-breed-summary__key-label").string
        value = item.find("dd", class_="m-breed-summary__value").string
        breed_card[key] = value
    breed_cards.append(breed_card)

df = pd.DataFrame(data=breed_cards)

df['count'] = 1
pivot_df = df.pivot_table(index='category', columns='Size', values='count', aggfunc='sum').fillna(0)

# streamlit bar_chart version
st.bar_chart(pivot_df)

# matplotlib version
ax = pivot_df.plot(kind='bar', stacked=True, figsize=(10, 6))
ax.set_xlabel('Category')
ax.set_ylabel('Count')
ax.set_title('Count by Category (stacked by Size)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

st.pyplot(ax.figure)

# altair version
import altair as alt

# group to compute counts per (category, Size)
grouped = df.groupby(['category', 'Size']).size().reset_index(name='count')

chart = (
    alt.Chart(grouped)
    .mark_bar()
    .encode(
        x=alt.X('category:N', sort=None, title='Category'),
        y=alt.Y('count:Q', title='Count'),
        color=alt.Color('Size:N', title='Size'),
        tooltip=['category', 'Size', 'count']
    )
    .properties(width=700, height=400)
)

st.altair_chart(chart, use_container_width=True)