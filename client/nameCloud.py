import base64
from io import BytesIO

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from datetime import date
from plotly.subplots import make_subplots
from wordcloud import WordCloud

from app import app, df

layout = html.Div([
    dcc.Graph(id='name-cloud-graph',
              config={'displayModeBar': False, 'staticPlot': True}),

    html.Div([
        html.Div([
            html.Div([
                'TOP',
                dcc.Slider(1, 150, 10,
                           # marks=None,
                           value=70,
                           id='name-cloud-input-th'),
            ],
                style={'width': '500px',
                       # 'display': 'inline-block',
                       'padding': '2px',
                       'margin': '0 auto'
                       }
            ),

            html.Div([
                html.Div([
                    'Start Year  ',
                    dcc.Input(id='name-cloud-input-year-start', type='number', value=2010)
                ],
                    style={'flex': 1
                           }
                ),
                html.Div([
                    'End Year  ',
                    dcc.Input(id='name-cloud-input-year-end', type='number', value=2020)
                ],
                    style={'flex': 1
                           }
                ),
            ],
                style={'width': '500px',
                       'display': 'flex',
                       'padding': '4px',
                       'margin': '0 auto',
                       # 'position': 'absolute',
                       # 'left': '310px',
                       }
            ),

            html.Div([
                dcc.Dropdown(
                    options=[
                            {"label": "Alabama", "value": "AL"},
                            {"label": "Alaska", "value": "AK"},
                            {"label": "Arizona", "value": "AZ"},
                            {"label": "Arkansas", "value": "AR"},
                            {"label": "California", "value": "CA"},
                            {"label": "Colorado", "value": "CO"},
                            {"label": "Connecticut", "value": "CT"},
                            {"label": "Delaware", "value": "DE"},
                            {"label": "District Of Columbia", "value": "DC"},
                            {"label": "Florida", "value": "FL"},
                            {"label": "Georgia", "value": "GA"},
                            {"label": "Hawaii", "value": "HI"},
                            {"label": "Idaho", "value": "ID"},
                            {"label": "Illinois", "value": "IL"},
                            {"label": "Indiana", "value": "IN"},
                            {"label": "Iowa", "value": "IA"},
                            {"label": "Kansas", "value": "KS"},
                            {"label": "Kentucky", "value": "KY"},
                            {"label": "Louisiana", "value": "LA"},
                            {"label": "Maine", "value": "ME"},
                            {"label": "Maryland", "value": "MD"},
                            {"label": "Massachusetts", "value": "MA"},
                            {"label": "Michigan", "value": "MI"},
                            {"label": "Minnesota", "value": "MN"},
                            {"label": "Mississippi", "value": "MS"},
                            {"label": "Missouri", "value": "MO"},
                            {"label": "Montana", "value": "MT"},
                            {"label": "Nebraska", "value": "NE"},
                            {"label": "Nevada", "value": "NV"},
                            {"label": "New Hampshire", "value": "NH"},
                            {"label": "New Jersey", "value": "NJ"},
                            {"label": "New Mexico", "value": "NM"},
                            {"label": "New York", "value": "NY"},
                            {"label": "North Carolina", "value": "NC"},
                            {"label": "North Dakota", "value": "ND"},
                            {"label": "Ohio", "value": "OH"},
                            {"label": "Oklahoma", "value": "OK"},
                            {"label": "Oregon", "value": "OR"},
                            {"label": "Pennsylvania", "value": "PA"},
                            {"label": "Rhode Island", "value": "RI"},
                            {"label": "South Carolina", "value": "SC"},
                            {"label": "South Dakota", "value": "SD"},
                            {"label": "Tennessee", "value": "TN"},
                            {"label": "Texas", "value": "TX"},
                            {"label": "Utah", "value": "UT"},
                            {"label": "Vermont", "value": "VT"},
                            {"label": "Virginia", "value": "VA"},
                            {"label": "Washington", "value": "WA"},
                            {"label": "West Virginia", "value": "WV"},
                            {"label": "Wisconsin", "value": "WI"},
                            {"label": "Wyoming", "value": "WY"}
                    ],
                    placeholder="Select a state",
                    id='name-cloud-input-state'
                )
            ],
                style={'width': '500px',
                       # 'display': 'inline-block',
                       'padding': '2px',
                       'margin': '0 auto',
                       # 'position': 'absolute',
                       # 'left': '310px',
                       }
            ),

            html.Div(
                id='name-cloud-graph-alert',
                children=[],
                style={
                    # 'display': 'inline-block',
                    'position': 'absolute',
                    'height': '50px',
                    'left': '200px',
                    'top': '60px'
                }
            ),

        ],
            style={
                'margin': '0 auto',
                'position': 'relative',
                'width': '500px'
            })
    ]),
],

)

alert = dbc.Alert("Please input year between 1910-2020!", color='danger', dismissable=False, duration=1500)


@app.callback(
    Output('name-cloud-graph', 'figure'),
    Output('name-cloud-graph-alert', 'children'),
    Input('name-cloud-input-year-start', 'value'),
    Input('name-cloud-input-year-end', 'value'),
    Input('name-cloud-input-th', 'value'),
    Input('name-cloud-input-state', 'value')
)
def update_figure(startYear, endYear, th, state):
    def get_most_named_data(syear, eyear, th, sex, state):
        filtered_df = df[(df['year'] >= syear) & (df['year'] <= eyear)]
        filtered_df = filtered_df[filtered_df['sex'] == sex]
        if state is not None:
            filtered_df = filtered_df[filtered_df['state_abb'] == state]
        names = filtered_df[['name', 'count']].groupby('name').sum()
        sort_names = names.sort_values(by='count', ascending=False)
        sort_names_th = sort_names.head(th)
        most_named = pd.Series(sort_names_th['count'].values, index=sort_names_th.index).to_dict()
        return most_named

    def get_name_cloud_image(dic, color):
        wc = WordCloud(background_color="white",
                       random_state=42, width=1500, height=1500,
                       colormap=color)
        nc = wc.generate_from_frequencies(dic)
        nc_img = nc.to_image()
        prefix = "data:image/png;base64,"
        with BytesIO() as buffer:
            nc_img.save(buffer, 'png')
            img = prefix + base64.b64encode(buffer.getvalue()).decode()
        return img

    if (startYear not in df.year.values and startYear is not None) or \
            (endYear not in df.year.values and endYear is not None):
        return [], alert
    startYear = int(startYear)
    endYear = int(endYear)
    th = int(th)

    most_named_f = get_most_named_data(startYear, endYear, th, 'F', state)
    most_named_m = get_most_named_data(startYear, endYear, th, 'M', state)
    f_img = get_name_cloud_image(most_named_f, 'autumn')
    m_img = get_name_cloud_image(most_named_m, 'winter')

    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(go.Image(source=f_img), 1, 1)
    fig.add_trace(go.Image(source=m_img), 1, 2)

    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    if startYear == endYear:
        title_text = str(th) + " most common female and male names in " + str(startYear)
    else:
        title_text = str(th) + " most common female and male names between " + str(startYear) + " and " + str(endYear)
    fig.update_layout(title_text=title_text)

    return fig, dash.no_update


if __name__ == '__main__':
    app.layout = layout
    app.run_server()
