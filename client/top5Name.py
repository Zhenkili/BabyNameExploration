import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from app import app, df

layout = html.Div([
    dcc.Graph(id='top5-name-graph'),

    html.Div([
        html.Div([
            html.Div([
                'TOP',
                dcc.Slider(1, 15, 1,
                           # marks=None,
                           value=10,
                           id='top5-name-input-th'),
            ],
                style={'width': '500px',
                       # 'display': 'inline-block',
                       'padding': '2px',
                       'margin': '0 auto'
                       }
            ),

            html.Div([
                dcc.RadioItems(
                    id='top5-name-input-sex',
                    options=[
                        {'label': 'Female', 'value': 'F'},
                        {'label': 'Male', 'value': 'M'},
                    ],
                    value='F',
                    labelStyle={"padding": "2px"},
                    inputStyle={"margin-right": "1px"}
                )
            ],
                style={'width': '500px',
                       # 'display': 'inline-block',
                       'margin': '0 auto',
                       }),

            html.Div([
                html.Div([
                    'Start Year  ',
                    dcc.Input(id='top5-name-input-year-start', type='number', value=2010)
                ],
                    style={'flex': 1
                           }
                ),
                html.Div([
                    'End Year  ',
                    dcc.Input(id='top5-name-input-year-end', type='number', value=2020)
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
                    id='top5-name-input-state'
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
                id='top5-name-the-alert',
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
    Output('top5-name-graph', 'figure'),
    Output('top5-name-the-alert', 'children'),
    Input('top5-name-input-year-start', 'value'),
    Input('top5-name-input-year-end', 'value'),
    Input('top5-name-input-sex', 'value'),
    Input('top5-name-input-th', 'value'),
    Input('top5-name-input-state', 'value')
)
def update_figure(startYear, endYear, sex, th, state):
    if (startYear not in df.year.values and startYear is not None) or \
            (endYear not in df.year.values and endYear is not None):
        return [], alert
    startYear = int(startYear)
    endYear = int(endYear)
    th = int(th)

    new_df = df
    if state is not None:
        new_df = df[(df['state_abb'] == state)]
    new_df = new_df[(new_df['year'] >= startYear) & (new_df['year'] <= endYear)]
    new_df = new_df[new_df['sex'] == sex]

    names = new_df.groupby(['name', 'sex'])['count'].sum().reset_index()
    sort_names = names.sort_values(by=['count'], ascending=False)
    sort_names_year_sex_th = sort_names.head(th)

    c = [i for i in range(th)]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=sort_names_year_sex_th['count'], y=sort_names_year_sex_th['name'],
                         orientation='h', marker=dict(color=c, colorscale='RdBu')))
    gender = 'Female' if sex == 'F' else 'Male'
    if startYear == endYear:
        title_text = "Top " + str(th) + " Popular " + gender + " Names in " + str(startYear)
    else:
        title_text = "Top " + str(th) + " Popular " + gender + " Names between " + str(startYear) + " and " + str(endYear)
    fig.update_layout(uniformtext_minsize=2, uniformtext_mode='hide', showlegend=False,
                      yaxis={'categoryorder': 'total ascending'},
                      plot_bgcolor='rgba(0,128,0,0.3)',
                      title_text=title_text)
    return fig, dash.no_update


if __name__ == '__main__':
    app.layout = layout
    app.run_server()
