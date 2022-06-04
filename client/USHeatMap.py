import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
# init_notebook_mode(connected=True)
from dash.dependencies import Input, Output

from app import app, df

layout = html.Div([
    dcc.Graph(id='us-heat-map-graph'),
    html.Div([
        html.Div([
            'Name ',
            dcc.Input(id='us-heat-map-input-name', type='text', value='Lily')
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
                id='us-heat-map-input-sex',
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
            'Year  ',
            dcc.Input(id='us-heat-map-input-year', type='number', value=2020)
        ],
            style={

                # 'display': 'inline-block',
                # 'position': 'absolute',
                # 'top': '60px',
                # 'left': '470px',
            }
        ),

        html.Div(
            id='us-heat-map-the-alert1',
            children=[],
            style={
                'position': 'absolute',
                # 'height': '50px',
                'top': '0px',
                'left': '200px',
            }
        ),

        html.Div(
            id='us-heat-map-the-alert2',
            children=[],
            style={'display': 'inline-block',
                   'position': 'absolute',
                   'height': '50px',
                   'top': '26px',
                   'left': '200px'
                   # 'left': '660px'
                   }
        ),
    ],
        style={'position': 'relative',
               'width': '500px',
               'margin': '0 auto'
               }
    ),

])

alert1 = dbc.Alert("Year between 1910-2020!", color='danger', dismissable=False, duration=1500)
alert2 = dbc.Alert("Invaild Name!", color='danger', dismissable=False, duration=1500)


@app.callback(
    Output('us-heat-map-graph', 'figure'),
    Output('us-heat-map-the-alert1', 'children'),
    Output('us-heat-map-the-alert2', 'children'),
    Input('us-heat-map-input-name', 'value'),
    Input('us-heat-map-input-sex', 'value'),
    Input('us-heat-map-input-year', 'value')
)
def update_figure(name, sex, year):
    name = name.capitalize()
    data = [dict(type='choropleth',
                 locationmode='USA-states',
                 autocolorscale=False,
                 marker=dict(
                     line=dict(color='rgb(255,255,255)', width=1)),
                 colorbar=dict(autotick=True, tickprefix='', title='Rank'),
                 reversescale=True,
                 )
            ]
    layout = dict(
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'),
    )
    fig = dict(data=data, layout=layout)
    # your validation here
    if year not in df.year.values and year != None:
        return fig, alert1, dash.no_update
    elif name not in df.name.values and name != None:
        return fig, dash.no_update, alert2
    elif year == None or year == '':
        return fig, dash.no_update, dash.no_update
    # year = int(year)
    sex_df = df.loc[df['sex'] == sex]
    year_sex_df = sex_df.loc[sex_df['year'] == year].groupby(['state_abb', 'name']).sum().drop(['year'], axis=1)
    all_states = df['state_abb'].unique()
    states_used = []
    rank_list = []
    for state in all_states:
        state_f = year_sex_df.loc[state].sort_values("count", ascending=False)['count']
        try:
            states_used.append(state)
            rank = np.where(state_f.index == name)[0] + 1
            if len(rank) == 0:
                rank_list.append(len(state_f))
            else:
                rank_list.append(rank[0])
        except:
            pass
    data = [dict(type='choropleth',
                 locations=states_used,
                 z=rank_list,
                 locationmode='USA-states',
                 text=states_used,
                 autocolorscale=False,
                 marker=dict(
                     line=dict(color='rgb(255,255,255)', width=1)),
                 colorbar=dict(autotick=True, tickprefix='', title='Rank'),
                 reversescale=True,
                 )
            ]
    layout = dict(
        title=f"" + name + " Name Rank in " + str(year),
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)'),
    )
    fig = dict(data=data, layout=layout)
    # fig2 = py.iplot(fig, validate=False, filename='USmap')
    return fig, dash.no_update, dash.no_update


if __name__ == '__main__':
    app.layout = layout
    app.run_server()
