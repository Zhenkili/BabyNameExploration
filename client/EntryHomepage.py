import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

import USHeatMap
import genderClassifier
import nameCloud
import nameTrend
import top5Name
from app import app

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.P(
            "US Newborn Naming Analysis", className="lead"
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Top Names", href="/", active="exact"),
                dbc.NavLink("US Name Cloud", href="/name-cloud", active="exact"),
                dbc.NavLink("Name Trend", href="/name-trend", active="exact"),
                dbc.NavLink("US Heat Map", href="/heat-map", active="exact"),
                dbc.NavLink("Gender Classifier", href="/gender-classifier", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return top5Name.layout
    elif pathname == "/name-cloud":
        return nameCloud.layout
    elif pathname == "/name-trend":
        return nameTrend.layout
    elif pathname == "/heat-map":
        return USHeatMap.layout
    elif pathname == "/gender-classifier":
        return genderClassifier.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False, port=8050)
