import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from app import app, df
from model import getGender

layout = html.Div([
    dcc.Graph(id='gender-classifier-graph'),

    html.Div([
        html.Div([
            html.Div([
                'Name ',
                dcc.Input(id='gender-classifier-input-name', type='text', value='Taylor')
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

        ],
            style={
                'margin': '0 auto',
                'position': 'relative',
                'width': '500px'
            })
    ]),
],

)

#alert = dbc.Alert("Please input year between 1910-2020!", color='danger', dismissable=False, duration=1500)


@app.callback(
    Output('gender-classifier-graph', 'figure'),
    Input('gender-classifier-input-name', 'value'),
)
def update_figure(name):
    name = name.capitalize()
    x = getGender(name)
    if x:
        gender = 'male'
    else:
        gender = 'female'
    name_df = df.loc[df['name'] == name].reset_index(drop=True)
    female_name_df = name_df.loc[name_df['sex'] == 'F']
    male_name_df = name_df.loc[name_df['sex'] == 'M']
    fig = go.Figure()
    male_baby_df = male_name_df.groupby('year').sum()
    female_baby_df = female_name_df.groupby('year').sum()
    fig.add_trace(go.Scatter(x=male_baby_df.index, y=male_baby_df['count'], name='Total Number of male babies'))
    fig.add_trace(go.Scatter(x=female_baby_df.index, y=female_baby_df['count'], name='Total Number of female babies'))
    fig.update_layout(title_text=name + " is most probably a " + gender + " name and the following is the trend over time",
                      yaxis_title="Value (log scale)")
    fig.update_yaxes(type="log")

    return fig


if __name__ == '__main__':
    app.layout = layout
    app.run_server()
