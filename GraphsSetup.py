import pandas as pd
import plotly.express as px
import GraphStyle as gs_style
import plotly.io as pio
from wordcloud import WordCloud

# Incorporate data
df = pd.read_excel(r"D:\_University\Fall 2025\games_excel.xlsx") # Change this based on who is running the code
#df = pd.read_csv('cleaned_games.csv', index_col=False)

# Style Setup

pio.templates["steam_template"] = gs_style.steam_template
pio.templates.default = "steam_template"

# Genre Popularity
# Handling Items ===================

df['Year released'] = pd.to_datetime(df['Release date'], errors='coerce').dt.year

# Count how many rows have invalid or missing release dates
invalid_dates_count = df['Year released'].isna().sum()
print(f"Number of rows with invalid or missing release dates: {invalid_dates_count}")

df.dropna(subset=['Year released'], inplace=True)
df['Year released'] = df['Year released'].astype(int)

# Handle Estimated Owners ===================
def parse_owners(owner_str):
    if isinstance(owner_str, str):
        try:
            low, high = owner_str.split(' - ')
            return (int(low) + int(high)) / 2
        except (ValueError, AttributeError):
            return None
    return None


# i had the change the key since there was a key error with just "Estimated owners". since there are three 
# different estimated owners columns, i just picked one but can change to whatever
df['Owners (numeric)'] = df['Estimated owners by cat'].apply(parse_owners)

# Positive Review Percentage ====================
df['Positive Review %'] = (df['Positive'] / (df['Positive'] + df['Negative'] + 1)) * 100

# Drop rows with 0 positive reviews for analysis
df = df[df['Positive'] > 0]

# Drop Rows with 0 negative reviews to avoid skewed percentages
df = df[df['Negative'] > 0]

df['total_reviews'] = df['Positive'] + df['Negative']
df = df[df.total_reviews > 0]

df_handled = df.copy()
# Genre popularity by release count over time
df_genre_analysis = df.copy()
df_genre_analysis.dropna(subset=['Genres'], inplace=True)

# Group by year, then apply a function to count genres for that year's subset.
genre_counts_by_year = df_genre_analysis.groupby('Year released')['Genres'].apply(
    lambda x: x.str.split(',').explode().value_counts()
).reset_index()
genre_counts_by_year.columns = ['Year released', 'Genre', 'Count']

# Find the top 10 genres overall to keep the chart clean.
total_genre_counts = genre_counts_by_year.groupby('Genre')['Count'].sum()
top_10_genres = total_genre_counts.nlargest(10).index

# Filter the yearly data to only include these top genres.
df_top_genres_yearly = genre_counts_by_year[genre_counts_by_year['Genre'].isin(top_10_genres)]

df_top_genres = df_genre_analysis[df_genre_analysis['Genres'].isin(top_10_genres)]
# Group by year and genre, then count the number of games
genre_counts_by_year = df_top_genres.groupby(['Year released', 'Genres']).size().reset_index(name='count')

genre_popularity_fig = px.line(
    genre_counts_by_year,
    x='Year released',
    y='count',
    color='Genres',
    title='Number of Game Releases Per Genre Over Time',
    labels={'Year released': 'Year of Release', 'count': 'Number of Games Released'},
    markers=True,
    hover_name='Genres',
    height=600
)


# Active Players Per Genre
# there isn't actually a way to show active players so uhh this will work for now
# could change to playtime last two weeks maybe
df_active_players = df.copy()
df_active_players = df_active_players[['Genres', 'Estimated owners by review']]

# converting strings into actual lists for parsing
def str_to_list(x):
    if isinstance(x, list):
        return x  # already a list
    elif isinstance(x, str):
        # Remove brackets if present
        x = x.strip("[]")
        if not x:
            return []
        # Split by comma and strip whitespace
        return [tag.strip() for tag in x.split(",")]
    else:
        return []  # for NaNs
    
df_active_players['Genres'] = df_active_players['Genres'].apply(str_to_list)
df_active_players = df_active_players.explode('Genres')
df_active_players = df_active_players.groupby('Genres', as_index=False)['Estimated owners by review'].sum()
df_active_players = df_active_players.sort_values(by='Estimated owners by review', ascending=False)

# only keep the top 10 genres
df_active_players = df_active_players.head(10)
# bar chart of players per genre
# hard to read genres vertically, so making horizontal
active_players_fig = px.bar(
    df_active_players, 
    y='Genres', 
    x='Estimated owners by review', 
    title='Estimated Owners Per Genre', 
    text='Estimated owners by review',
    orientation='h')


# Bubble Chart
df_bubble = df.copy()
df_bubble = df_bubble[['Genres', 'Average playtime forever', 'Positive Review %']]
df_bubble['Genres'] = df_bubble['Genres'].apply(str_to_list)
df_bubble = df_bubble.explode('Genres')
df_bubble = df_bubble.groupby('Genres', as_index=False).agg({
    'Average playtime forever': 'mean',
    'Positive Review %': 'mean'
})
df_bubble = df_bubble.sort_values(by='Positive Review %', ascending=False)
# only keep the top 10 genres by review
df_bubble = df_bubble.head(10)
# size will be count of games in that genre
genre_counts = df_bubble['Genres'].value_counts().reset_index()
genre_counts.columns = ['Genres', 'count']
print(genre_counts)
df_bubble = pd.merge(df_bubble, genre_counts, on='Genres')
bubble_fig = px.scatter(
    df_bubble, 
    x='Average playtime forever', 
    y='Positive Review %', 
    size='count', 
    color='Genres', 
    hover_name='Genres', 
    title='Average Playtime vs Positive Review % per Genre',
    size_max=60)
# need to change the values on this because everything is 1 so there is no size 
# difference but good enough for now surely


# Genre Word Cloud
df_wc = df.copy()
df_wc = df_wc['Genres']


df_wc = df_wc.apply(str_to_list)
df_wc = df_wc.explode()
wc_count = df_wc.value_counts().reset_index()

wc_dict = {}
for k, v in zip(wc_count['Genres'], wc_count['count']):
    wc_dict[k] = int(v)

wc = WordCloud(
    width=800, 
    height=600, 
    background_color="#171a21", 
    colormap="Blues").generate_from_frequencies(wc_dict)
wc_fig = px.imshow(wc, aspect="auto")
wc_fig.update_layout(xaxis_title='', yaxis_title='', xaxis=dict(visible=False), yaxis=dict(visible=False))

