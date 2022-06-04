import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from app import app, df

layout = html.Div([

    dcc.Graph(id='name-trend-graph'),
    html.Div([
        html.Div([
            "Name: ",
            dcc.Input(id='name-trend-input-name', value='James', type='text')
        ],
            style={
                # 'display': 'inline-block',
                # 'position':'absolute',
                'padding': '2px',
                'margin': '4px 0 4px',
                # 'margin': '15px auto',
                # 'top': '12px',
                # 'left': '470px'

            }
        ),

        html.Div([
            dcc.RadioItems(
                id='name-trend-input-sex',
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
                id='name-trend-input-state'
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
            id='name-trend-the-alert',
            children=[],
            style={'display': 'inline-block',
                   'position': 'absolute',
                   'height': '50px',
                   'left': '380px'
                   }
        ),
    ],
        style={
            'width': '500px',
            'height': '30px',
            'margin': '0 auto',
            'position': 'relative'
        }),



])

alert = dbc.Alert("Invalid Name!", color="danger", dismissable=False, duration=1500)


@app.callback(
    Output('name-trend-graph', 'figure'),
    Output('name-trend-the-alert', 'children'),
    Input('name-trend-input-name', 'value'),
    Input('name-trend-input-sex', 'value'),
    Input('name-trend-input-state', 'value'))
def update_figure(name, sex, state):
    name = name.capitalize()
    if name not in df.name.values and name != '':  # if illegal, make graph blank and show alert
        return [], alert
    new_df = df
    if state is not None:
        new_df = df[(df['state_abb'] == state)]

    name_df = new_df.loc[new_df['name'] == name].reset_index(drop=True)
    sex_name_df = name_df.loc[name_df['sex'] == sex]
    sex_df = new_df.loc[new_df['sex'] == sex].groupby(['year', 'name']).sum()

    all_years = new_df['year'].unique()
    years_used = []
    rank_list = []
    for year in all_years:
        year_f = sex_df.loc[year].sort_values("count", ascending=False)['count']
        try:
            years_used.append(year)
            rank = (np.where(year_f.index == name)[0] + 1) / len(year_f)
            if len(rank) == 0:
                rank_list.append(0)
            else:
                rank_list.append(1 - rank[0])
        except:
            pass

    fig = go.Figure()
    year_sex_name_df = sex_name_df.groupby('year').sum()
    fig.add_trace(go.Scatter(x=year_sex_name_df.index, y=year_sex_name_df['count'], name='Total Number'))
    fig.add_trace(go.Bar(x=years_used, y=rank_list, name='Popularity'))
    fig.update_layout(title={'text': f"Trend of " + name + " Over Time", 'x': 0.5,
                             'xanchor': 'center', 'font': {'size': 20}}, xaxis_title="Year",
                      yaxis_title="Value (log scale)")
    fig.update_yaxes(type="log")

    return fig, dash.no_update


if __name__ == '__main__':
    app.layout = layout
    app.run_server()
