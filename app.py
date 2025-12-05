from dash import dash, html, dcc, html
import dash_ag_grid as dag
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
import GraphsSetup as gs

# ------------------- PLotly Figures and Data -------------------- #

# Homepage Figures
Fig1 = gs.genre_popularity_fig
Fig2 = gs.active_players_fig
Fig3 = gs.bubble_fig
Fig4 = gs.wc_fig
Fig5 = gs.scatterplot_fig

# ------------------- DASH APP SETUP -------------------- #
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
                        html.H2("Game Releases Over Time", className="card-title"),
                        html.P("(line chart)", className="card-subtitle"),
                    ]),
                    html.Div(className="actual-content", children=[
                        dcc.Graph(figure=Fig1, responsive=True)
                    ]),
                    # html.Div("Line Chart Placeholder", className="placeholder-content"), # ======== Insert Chart Here =========
                ]),
                html.Div(className="card", children=[
                    html.Div(className="card-header", children=[
                        html.H2("Active Players Per Genre", className="card-title"),
                        html.P("(bar chart)", className="card-subtitle"),
                    ]),
                    html.Div(className="actual-content", children=[
                        dcc.Graph(figure=Fig2, responsive=True)
                    ]),
                    #html.Div("Bar Chart Placeholder", className="placeholder-content"), # ======== Insert Chart Here =========
                ]),
                html.Div(className="card", children=[
                    html.Div(className="card-header", children=[
                        html.H2("Genre Explore", className="card-title"),
                        html.P("(bubble chart)", className="card-subtitle"),
                    ]),
                    html.Div(className="actual-content", children=[
                        dcc.Graph(figure=Fig3, responsive=True)
                    ]),
                    #html.Div("Bubble Chart Placeholder", className="placeholder-content"), # ======== Insert Chart Here =========
                ]),
                html.Div(className="card", children=[
                    html.Div(className="card-header", children=[
                        html.H2("Top Performing Tags", className="card-title"),
                        html.P("(word cloud)", className="card-subtitle"),
                    ]),
                    html.Div(className="actual-content", children=[
                        dcc.Graph(figure=Fig4, responsive=True)
                    ]),
                    #html.Div("Word Cloud Placeholder", className="placeholder-content"), # ======== Insert Chart Here =========
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
                    html.Div(className="actual-content", children=[
                        dcc.Graph(figure=Fig5, id='main-scatter-plot', style={'height': '100%', 'width': '100%'})
                    ]),
                ]),
            ],
        ),
    ],
)


# ---------------- LAYOUT FOR THE GAME DETAILS PAGE ---------------- #
# Had to turn into function for dynamic page
def layout_detail(game_id):
    
    # Logic to find the specific game details based on ID
    
    game_df = gs.get_game_data(game_id)
    
    if game_df is None or game_df.empty:
        return html.Div(
            className="detail-page",
            children=[html.H1("Game not found", style={"color": "white", "text-align": "center"})]
        )

    name = game_df['Name'].iloc[0]
    price = game_df.get('Price_Formatted', "N/A").iloc[0]
    description = game_df.get('About the game', "No description").iloc[0]
    image_url = game_df.get('Website', "").iloc[0]
    release_date = game_df.get('Release Date', "N/A").iloc[0]
    developer = game_df.get('Developers', "N/A").iloc[0]
    publisher = game_df.get('Publishers', "N/A").iloc[0]
    total_number_reviews = game_df.get('Total number of reviews', "N/A").iloc[0]
    genres = game_df.get('Genres', "N/A").iloc[0]
    avg_playtime = game_df.get('Average playtime forever', "N/A").iloc[0]
    achievements = game_df.get('Achievements', "N/A").iloc[0]
    
    # Figures
    radar_fig = gs.radar_chart(game_df)
    
    # Create the chart content conditionally
    radar_chart_content = (
        dcc.Graph(figure=radar_fig, responsive=True, config={'displayModeBar': False})
        if radar_fig is not None
        else html.Div("No data available for chart", className="placeholder-content")
    )

    steam_widget = html.Iframe(
    src=f"https://store.steampowered.com/widget/{game_id}/",
    style={
        "border": "none",
        "width": "95%", 
        "height": "190px", # Standard steam widget height
        "overflow": "hidden",
        "margin-top": "20px"
    }
)

    return html.Main(
        className="detail-page",
        children=[
            # Top Section
            html.Section(
                className="game-summary-section",
                children=[
                    html.Div(className="game-cover", children = [
                        html.Img(src=image_url, alt=name)
                    ]),
                    html.Div(
                        className="game-info",
                        children=[
                            # Use the dynamic title here
                            html.H1(name), 
                            html.P("Price: " + str(price), className="price"),
                            html.P("Genres: " + genres, id="genres", className="genres"),
                            html.Div(
                                className="description-box",
                                children=[
                                    html.H2("Description", className="description-title"),
                                    html.P(str(description)) 
                                ]
                            ),  
                        ],
                    ),
                    html.Div(
                        className="game-stats",
                        children=[
                            # Display the ID dynamically
                            html.Div(className="stat-card", children=[html.Div("App ID", className="label"), html.Div(str(game_id), className="value")]),
                            html.Div(className="stat-card", children=[html.Div("Avg Playtime", className="label"), html.Div(str(avg_playtime) + " Minutes", className="value")]),
                            html.Div(className="stat-card", children=[html.Div("Total Reviews", className="label"), html.Div(str(total_number_reviews), className="value")]),
                            html.Div(className="stat-card", children=[html.Div("Achievements", className="label"), html.Div(str(achievements), className="value")]),
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
                            html.Div(className="actual-content", children=[radar_chart_content]),
                            #html.Div("Info Chart Placeholder", className="placeholder-content"),
                        ],
                    ),
                    html.Div(
                        className="card",
                        children=[
                            html.Div(className="card-header", children=[html.H2("Steam Link", className="card-title")]),
                            html.Div(className="actual-content", children=[steam_widget])
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
            # Left side: Navigation Links
            html.Div(
                className="nav-links",
                children=[
                    dcc.Link("Home", href="/"),
                    html.Span(" | ", className="separator"), # distinct separator for styling
                    html.Button(
                        "Random Game", 
                        id="btn-random-game", 
                        className="nav-btn-link"
                    ),
                ]
            ),

            # Center: Search Bar
            html.Div(
                className="search-wrapper",
                children=[
                    dcc.Dropdown(
                        id='game-search-dropdown',
                        options=gs.search_options,
                        placeholder="Search for a game...",
                        searchable=True,
                        clearable=True,
                        className="steam-dropdown" # Custom class for CSS targeting
                    )
                ]
            ),
            
            # Right side: Empty div to help balance the flexbox centering (optional, but good for symmetry)
            html.Div(className="nav-spacer") 
        ],
    ),
    # The 'page-content' div is where the layout for each page will be rendered
    html.Div(id='page-content')
])

# This callback changes the content of 'page-content' based on the URL
# 1. Routing Callback (Handles Home vs Detail views)
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/detail':
        # Now this works because layout_detail is a function
        return layout_detail("Example") 
        
    elif pathname and pathname.startswith('/game/'):
        try:
            game_id = pathname.split('/')[-1]
            # This passes the ID to the function we just created
            return layout_detail(game_id) 
        except:
            return layout_detail("Error")
            
    else:
        return layout_home

# 2. CLICK INTERACTION CALLBACK
# This listens to the scatter plot and updates the URL
@app.callback(
    Output('url', 'pathname'),
    Input('main-scatter-plot', 'clickData')
)
def update_url_on_click(clickData):
    if not clickData:
        return dash.no_update

    try:
        # 1. Get the hover text (which is now "Name___ID")
        point = clickData['points'][0]
        
        # 'hovertext' is standard when using hover_name
        full_text = point.get('hovertext', '') 
        
        print(f"Hover text: {full_text}")

        if '___' in full_text:
            # 2. Split the string and take the last part (the ID)
            game_id = full_text.split('___')[-1]
            return f"/game/{game_id}"
        else:
            print("Separator '___' not found in hover text")
            return dash.no_update

    except Exception as e:
        print(f"Error parsing click data: {e}")
        return dash.no_update
    
# 3. SEARCH BAR CALLBACK
@app.callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('game-search-dropdown', 'value'),
    prevent_initial_call=True
)
def update_url_on_search(game_id):
    if game_id:
        # Navigate to the specific game page
        return f"/game/{game_id}"
    return dash.no_update

# 4. Random Game Callback
@app.callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('btn-random-game', 'n_clicks'),
    prevent_initial_call=True
)
def go_to_random_game(n_clicks):
    if n_clicks:
        random_id = gs.get_random_game_id()
        return f"/game/{random_id}"
    return dash.no_update

if __name__ == '__main__':
    app.run(debug=True)