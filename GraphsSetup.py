import pandas as pd
import plotly.express as px
import GraphStyle as gs_style
import plotly.io as pio
from wordcloud import WordCloud
import random

# Incorporate data
# df = pd.read_excel(r"D:\_University\Fall 2025\cleaned_games.csv") # Change this based on who is running the code
df = pd.read_csv('cleaned_games.csv', index_col=False)
HeaderimagesTable = pd.read_csv('gamesHeaderImagesTable.csv', index_col=False)

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

# ========== Search Bar Setup =============
df_search = df[['Name', 'AppID']].dropna().drop_duplicates(subset=['AppID'])

# Format for dcc.Dropdown: [{'label': 'Game Name', 'value': 123}]
search_options = [
    {'label': str(row['Name']), 'value': row['AppID']} 
    for index, row in df_search.iterrows()
]

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

genre_popularity_fig.update_layout(
    autosize=True,
    title_x=0.05
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
df_active_players['Genres'] = df_active_players['Genres'].replace('Massively Multiplayer', 'MMO')
df_active_players['Genres'] = df_active_players['Genres'].replace('Free to Play', 'F2P')
# bar chart of players per genre
# hard to read genres vertically, so making horizontal
active_players_fig = px.bar(
    df_active_players, 
    y='Genres', 
    x='Estimated owners by review', 
    title='Estimated Owners Per Genre', 
    text='Estimated owners by review')

active_players_fig.update_layout(
    autosize=True,
    title_x=0.05,
    margin=dict(l=100)
    
)


# Bubble Chart
# x: avg playtime forever, y: recommendations, size: total reviews, color: genre
df_bubble = df.copy()
df_bubble = df_bubble[['Genres', 'Average playtime forever', 'Recommendations', 'Total number of reviews', 'AppID']]
# remove 0s
df_bubble = df_bubble[(df_bubble['Average playtime forever'] > 0) & (df_bubble['Recommendations'] > 0) & (df_bubble['Total number of reviews'] > 0)]
df_bubble['Genres'] = df_bubble['Genres'].apply(str_to_list)
df_bubble = df_bubble.explode('Genres')

bubble_stats = df_bubble.groupby('Genres').agg({'Average playtime forever': 'mean',
    'Recommendations': 'mean',
    'Total number of reviews': 'sum',
    'AppID': 'count'  # to count number of games per genre
}).reset_index()

bubble_stats.rename(columns={'AppID': 'Number of games'}, inplace=True)

top_genres = bubble_stats.nlargest(10, 'Number of games')


bubble_fig = px.scatter(
    top_genres, 
    x='Average playtime forever', 
    y='Recommendations', 
    size='Total number of reviews', 
    color='Genres', 
    hover_name='Genres',
    hover_data={
        'Average playtime forever': ':.1f',
        'Recommendations': ':,.0f',
        'Total number of reviews': ':,',
        'Number of games': ':,',
        'Genres': False
        }, 
    title='Game Engagement by Genre',
    size_max=60
    )

bubble_fig.update_layout(
    autosize=True,
    title_x=0.05
)




# Genre Word Cloud
df_wc = df.copy()
df_wc = df_wc['Tags']

df_wc = df_wc.apply(str_to_list)
df_wc = df_wc.explode()
wc_count = df_wc.value_counts().reset_index()

wc_dict = {}
for k, v in zip(wc_count['Tags'], wc_count['count']):
    wc_dict[k] = int(v)

wc = WordCloud(
    width=1000, 
    height=800, 
    background_color="#171a21", 
    colormap="Blues").generate_from_frequencies(wc_dict)
wc_fig = px.imshow(wc, aspect="auto")
wc_fig.update_layout(xaxis_title='', yaxis_title='', xaxis=dict(visible=False), yaxis=dict(visible=False))
wc_fig.update_traces(hoverinfo='skip', hovertemplate=None) # removing info on hover bc doesnt show anything

df_handled['Clickable_Info'] = df_handled['Name'] + "___" + df_handled['AppID'].astype(str)

scatterplot_fig = px.scatter(
    df_handled,
    x='Average playtime forever',
    y='Positive Review %',
    hover_name='Clickable_Info',
    title='Average Playtime vs Positive Review % (Click a point)',
    size_max=60,
    # custom_data=['AppID'],
    hover_data={'AppID': True},
    render_mode='webgl'
)

# Detail Page Function
def get_game_data(game_id):
    """
    Takes a game_id (int or str), finds the matching row in the global df,
    and returns a DataFrame containing the single row.
    Returns None if no game is found.
    """
    try:
        # 1. Ensure ID is an integer for comparison
        target_id = int(game_id)
    except (ValueError, TypeError):
        print(f"Invalid Game ID format: {game_id}")
        return None

    
    # We use .copy() to avoid SettingWithCopy warnings if we modify it later
    game_row = df[df['AppID'] == target_id].copy()

    if game_row.empty:
        print(f"Game ID {target_id} not found in dataset.")
        return None

    # Read Table for Header Images
    website_data = HeaderimagesTable[['AppID', 'Website']]
    game_row = pd.merge(game_row, website_data, on='AppID', how='left')
    
    if 'Website' not in game_row.columns:
        game_row['Website'] = "N/A"

    # Release Date
    if 'Release Date' not in game_row.columns:
        game_row['Release Date'] = "N/A"
    
    # If 'About the game' (description) is missing
    if 'About the game' not in game_row.columns:
        game_row['About the game'] = "No description available for this title."

    # Format Price 
    if 'Price' in game_row.columns:
        # formatting as currency string for display
        val = game_row['Price'].values[0]
        game_row['Price_Formatted'] = "Free" if val == 0 else f"${val:.2f}"
    else:
        game_row['Price_Formatted'] = "N/A"

    return game_row

# used for radar chart scaling
PLAYTIME_MAX = df['Average playtime forever'].quantile(0.95)
REVIEWS_MAX = df['total_reviews'].quantile(0.95)
RECOMMENDATIONS_MAX = df['Recommendations'].quantile(0.95)
ACHIEVEMENTS_MAX = df['Achievements'].quantile(0.95)

# charts for game detail page based on AppID
def radar_chart(game_data):
    if game_data is None:
        print("data is None")
        return None
    
    if game_data.empty:
        print("data is empty")
        return None
    
    try:

        categories = ['Positive Review %', 'Average playtime forever', 'Total number of reviews', 'Recommendations', 'Achievements']
    
        positive_review = game_data['Positive Review %'].values[0]
        avg_playtime = game_data['Average playtime forever'].values[0]
        total_reviews = game_data['total_reviews'].values[0]
        recommendations = game_data['Recommendations'].values[0]
        achievements = game_data['Achievements'].values[0]
    
        # normalize based on global max
        values = [
            positive_review,
            min((avg_playtime / PLAYTIME_MAX) * 100, 100),
            min((total_reviews / REVIEWS_MAX) * 100, 100),
            min((recommendations / RECOMMENDATIONS_MAX) * 100, 100), 
            min((achievements / ACHIEVEMENTS_MAX) * 100, 100)
        ]

        radar_fig = px.line_polar(
            r=values + [values[0]],  # close the loop
            theta=categories + [categories[0]],
            line_close=True,
            title=f"Game Metrics Radar Chart for {game_data['Name'].values[0]}",
        )

        radar_fig.update_traces(fill='toself')
        radar_fig.update_layout(
            autosize=True,
            title_x=0.05,
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    ticksuffix='%'
                )
            )
        )

        return radar_fig
    except Exception as e:
        print(f"Error creating radar chart: {e}")
        return None
    
def get_random_game_id():
    """Returns a random AppID from the dataset"""
    # Get a list of all unique IDs
    all_ids = df['AppID'].unique()
    # Pick one
    return random.choice(all_ids)