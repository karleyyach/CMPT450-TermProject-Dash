import pandas as pd
import plotly.express as px
import GraphStyle as gs_style
import plotly.io as pio

# Incorporate data
df = pd.read_excel(r"D:\_University\Fall 2025\games_excel.xlsx") # Change this based on who is running the code


# Style Setup

pio.templates["steam_template"] = gs_style.steam_template
pio.templates.default = "steam_template"


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

df['Owners (numeric)'] = df['Estimated owners'].apply(parse_owners)

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



