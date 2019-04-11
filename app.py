#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

SCOTLAND_DATA = pd.read_csv(
    'https://raw.githubusercontent.com/asongtoruin/baby_dash/master'
    '/Filtered%20Names%20Scotland.csv'
)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Scottish Baby Names'
server = app.server

app.layout = html.Div(children=[
    html.H1('Scottish Baby Names', style={'textAlign': 'center'}),
    html.Div(
        'Select a name to view the number of babies given this name in '
        'Scotland between 1974 and 2018 (only names appearing more than 10 '
        'times in that period are shown)'),
    dcc.Dropdown(
        id='name-chooser',
        options=[{'label': n, 'value': n}
                 for n in sorted(SCOTLAND_DATA['Name'].unique())],
        value='Adam', multi=False
    ),
    dcc.Loading(
        id='graph-loading', type='graph',
        children=[dcc.Graph(id='baby-name-graph')]
    )
])

@app.callback(Output('baby-name-graph', 'figure'),
              [Input('name-chooser', 'value')])
def baby_name_stats(chosen_name):
    baby_data = SCOTLAND_DATA[SCOTLAND_DATA['Name'].eq(chosen_name)]

    traces = []
    traces.append(
        go.Scatter(
            x=baby_data['Year'],
            y=baby_data['Assigned Male'],
            name='Assigned Male',
            mode='markers'
        )
    )
    traces.append(
        go.Scatter(
            x=baby_data['Year'],
            y=baby_data['Assigned Female'],
            name='Assigned Female',
            mode='markers'
        )
    )

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Year', 'range': [1973, 2019]},
            yaxis={'title': 'Number of births', 'rangemode': 'nonnegative'},
            legend={'orientation': 'h', 'xanchor': 'center', 'x': 0.5, 'y': -0.3}
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
