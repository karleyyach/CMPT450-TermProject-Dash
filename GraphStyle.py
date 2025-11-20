import GraphsSetup

#
# --- PLOTLY GRAPH STYLING TEMPLATE ---
#
steam_template = {
    "layout": {
        # --- BACKGROUNDS ---
        "paper_bgcolor": "#1b2838",  # --bg-panel: Background of the entire chart area
        "plot_bgcolor": "#171a21",   # --bg-main: Background of the plotting area

        # --- FONTS ---
        "font": {
            "family": "Poppins, sans-serif", # --font-family
            "color": "#c7d5e0",              # --text-light: Default text color
            "size": 12
        },
        "title": {
            "font": {
                "color": "#ffffff",          # --text-bright: Title text color
                "size": 18
            },
            "x": 0.5, # Align title to center
            "xanchor": "left"
        },
        "legend": {
            "bgcolor": "rgba(27, 40, 56, 0.7)", # --bg-panel with transparency
            "bordercolor": "#263445",          # --border-color
            "borderwidth": 1
        },

        # --- AXES ---
        "xaxis": {
            "gridcolor": "#263445",     # --border-color: Color of grid lines
            "linecolor": "#263445",     # --border-color: Color of the axis line
            "zerolinecolor": "#8a99a4"  # --text-muted: Color of the zero line
        },
        "yaxis": {
            "gridcolor": "#263445",
            "linecolor": "#263445",
            "zerolinecolor": "#8a99a4"
        },

        # --- COLOR SCALES ---
        # Defines the default color sequence for traces (lines, bars, etc.)
        "colorway": ["#66c0f4", "#70e0a8", "#f4b466", "#e07070", "#a870e0", "#ffffff"], # Start with --primary-accent
    }
}