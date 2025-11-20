from dash import dash, html, dcc, html
import dash_ag_grid as dag
import pandas as pd
from dash.dependencies import Input, Output


# Incorporate data
df = pd.read_excel(r"D:\_University\Fall 2025\games_excel.xlsx") # Change this based on who is running the code



external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap",
        "rel": "stylesheet",
    },
]
# Initialize the Dash app
# suppress_callback_exceptions is needed for multi-page apps
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)

# The title that appears in the browser tab
app.title = "Next Play - Game Data Dashboard"

# ------------------ LAYOUT FOR THE HOME PAGE ------------------ #
layout_home = html.Main(
    className="dashboard",
    children=[
        # Top row of charts
        html.Section(
            className="top-charts",
            children=[
                html.Div(className="card", children=[
                    html.Div(className="card-header", children=[
                        html.H2("Active Players Over Time", className="card-title"),
                        html.P("(line chart)", className="card-subtitle"),
                    ]),
                    html.Div("Line Chart Placeholder", className="placeholder-content"),
                ]),
                html.Div(className="card", children=[
                    html.Div(className="card-header", children=[
                        html.H2("Active Players Per Genre", className="card-title"),
                        html.P("(bar chart)", className="card-subtitle"),
                    ]),
                    html.Div("Bar Chart Placeholder", className="placeholder-content"),
                ]),
                html.Div(className="card", children=[
                    html.Div(className="card-header", children=[
                        html.H2("Genre Explore", className="card-title"),
                        html.P("(bubble chart)", className="card-subtitle"),
                    ]),
                    html.Div("Bubble Chart Placeholder", className="placeholder-content"),
                ]),
                html.Div(className="card", children=[
                    html.Div(className="card-header", children=[
                        html.H2("Top Performing Tags", className="card-title"),
                        html.P("(word cloud)", className="card-subtitle"),
                    ]),
                    html.Div("Word Cloud Placeholder", className="placeholder-content"),
                ]),
            ],
        ),
        # Bottom section with filters and main chart
        html.Section(
            className="bottom-content",
            children=[
                # Filters panel
                html.Aside(className="filters-panel", children=[
                    html.H3("Filters"),
                    html.Div(className="filter-group", children=[
                        html.Label("Genres", htmlFor="genre-select"),
                        html.Div(className="custom-select-wrapper", children=[
                            dcc.Dropdown(
                                id="genre-select",
                                options=[
                                    {"label": "All Genres", "value": "all"},
                                    {"label": "Action", "value": "action"},
                                    {"label": "Adventure", "value": "adventure"},
                                    {"label": "RPG", "value": "rpg"},
                                    {"label": "Strategy", "value": "strategy"},
                                    {"label": "Simulation", "value": "simulation"},
                                ],
                                value="all",
                                clearable=False
                            )
                        ]),
                    ]),
                    # Crazy way of doing this, but gemini kept doing this so whatever atm
                    # html.Div(className="filter-group", children=[
                    #     html.Label("Price Range", htmlFor="price-range"),
                    #     html.Div(className="range-slider-wrapper", children=[
                    #         dcc.RangeSlider(id='price-range', min=0, max=100, step=1, value=[50])
                    #     ]),
                    # ]),
                    # html.Div(className="filter-group", children=[
                    #     html.Label("Release Date", htmlFor="release-date"),
                    #     html.Div(className="range-slider-wrapper", children=[
                    #         dcc.RangeSlider(id='release-date', min=2000, max=2024, step=1, value=[2018])
                    #     ]),
                    # ]),
                ]),
                # Main chart area
                html.Div(className="card main-chart", children=[
                    html.Div(className="placeholder-content", children=[
                        "Main Scatter Plot Placeholder",
                        html.Div(className="faux-tooltip", children=[
                            html.Div("Game Name", className="name"),
                            html.Div("Price", className="price"),
                            html.Div("→", className="arrow"),
                        ]),
                    ]),
                ]),
            ],
        ),
    ],
)


# ---------------- LAYOUT FOR THE GAME DETAILS PAGE ---------------- #
layout_detail = html.Main(
    className="detail-page",
    children=[
        # Top Section
        html.Section(
            className="game-summary-section",
            children=[
                html.Div("Game Cover", className="game-cover"),
                html.Div(
                    className="game-info",
                    children=[
                        html.H1("Game Title"),
                        html.P("$19.99", className="price"),
                        html.P("Action, Adventure, Indie", className="genres"),
                        html.P(
                            "This is a placeholder description for the game. It provides a brief summary of the gameplay, story, and key features to give players an idea of what to expect.",
                            className="description",
                        ),
                    ],
                ),
                html.Div(
                    className="game-stats",
                    children=[
                        html.Div(className="stat-card", children=[html.Div("Achievements", className="label"), html.Div("42", className="value")]),
                        html.Div(className="stat-card", children=[html.Div("Avg Playtime", className="label"), html.Div("86", className="value")]),
                        html.Div(className="stat-card", children=[html.Div("Developer", className="label"), html.Div("DevCo", className="value")]),
                        html.Div(className="stat-card", children=[html.Div("Positive Review %", className="label"), html.Div("92%", className="value")]),
                        html.Div(className="stat-card", children=[html.Div("Publisher", className="label"), html.Div("PubStaging", className="value")]),
                        html.Div(className="stat-card", children=[html.Div("Est. Owners", className="label"), html.Div("1.2M", className="value")]),
                    ],
                ),
            ],
        ),
        # Bottom Section
        html.Section(
            className="bottom-section",
            children=[
                html.Div(
                    className="card",
                    children=[
                        html.Div(className="card-header", children=[html.H2("Info Chart", className="card-title")]),
                        html.Div("Info Chart Placeholder", className="placeholder-content"),
                    ],
                ),
                html.Div(
                    className="card",
                    children=[
                        html.Div(
                            className="card-header",
                            children=[
                                html.H2("Comparison to Aspects of Popularity", className="card-title"),
                                html.P("(radar chart)", className="card-subtitle"),
                            ],
                        ),
                        html.Div("Radar Chart Placeholder", className="placeholder-content"),
                    ],
                ),
                html.Div(
                    className="card similar-games",
                    children=[
                        html.Div(className="card-header", children=[html.H2("Similar Games", className="card-title")]),
                        html.Div(
                            className="similar-games-list",
                            children=[
                                html.Div(className="similar-game-item", children=[
                                    html.Div(className="similar-game-cover"),
                                    html.Div(className="similar-game-info", children=[
                                        html.Div("Another Great Game", className="name"),
                                        html.Div("Indie, RPG", className="genres"),
                                        html.Div("A short description of a similar game goes here.", className="description"),
                                    ]),
                                ]),
                                html.Div(className="similar-game-item", children=[
                                    html.Div(className="similar-game-cover"),
                                    html.Div(className="similar-game-info", children=[
                                        html.Div("GameQuest Saga", className="name"),
                                        html.Div("Adventure", className="genres"),
                                        html.Div("Another short description text for the list item.", className="description"),
                                    ]),
                                ]),
                                html.Div(className="similar-game-item", children=[
                                    html.Div(className="similar-game-cover"),
                                    html.Div(className="similar-game-info", children=[
                                        html.Div("Strategy Masters", className="name"),
                                        html.Div("Strategy, Simulation", className="genres"),
                                        html.Div("Final game description in this placeholder list.", className="description"),
                                    ]),
                                ]),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# ------------------ MAIN APP LAYOUT AND ROUTING ------------------ #
app.layout = html.Div([
    # dcc.Location is used to track the browser's URL
    dcc.Location(id='url', refresh=False),

    # The top navigation bar will be present on all pages
    html.Div(
        className="top-bar",
        children=[
            dcc.Link("| Home |", href="/"), # Use "/" for the root/home page
            dcc.Link(" Game Details |", href="/detail"),
        ],
    ),
    
    # The 'page-content' div is where the layout for each page will be rendered
    html.Div(id='page-content')
])

# This callback changes the content of 'page-content' based on the URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/detail':
        return layout_detail
    else: # Default to home page
        return layout_home


# --------------------------- RUN THE APP --------------------------- #



if __name__ == '__main__':
    app.run(debug=True)
