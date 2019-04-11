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

STANDARD_LAYOUT = go.Layout(
    xaxis={'title': 'Year', 'range': [1973, 2019]},
    yaxis={'title': 'Number of births', 'rangemode': 'nonnegative'},
    legend={'orientation': 'h', 'xanchor': 'center', 'x': 0.5, 'y': -0.3}
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
    html.H2('One Name by Gender'),
    dcc.Dropdown(
        id='single-name-chooser',
        options=[{'label': n, 'value': n}
                 for n in sorted(SCOTLAND_DATA['Name'].unique())],
        value='Adam', multi=False
    ),
    dcc.Loading(
        id='graph-loading', type='graph',
        children=[dcc.Graph(id='baby-name-graph')]
    ),
    html.H2('Compare Name Totals'),
    dcc.Dropdown(
        id='multiple-name-chooser',
        options=[{'label': n, 'value': n}
                 for n in sorted(SCOTLAND_DATA['Name'].unique())],
        value='Adam', multi=True
    ),
    dcc.Loading(
        id='comparison-graph-loading', type='graph',
        children=[dcc.Graph(id='comparison-name-graph')]
    )
])


@app.callback(Output('baby-name-graph', 'figure'),
              [Input('single-name-chooser', 'value')])
def one_baby_name(chosen_name):
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
        'layout': STANDARD_LAYOUT
    }


@app.callback(Output('comparison-name-graph', 'figure'),
              [Input('multiple-name-chooser', 'value')])
def one_baby_name(chosen_names):
    traces = []
    if not chosen_names:
        return dict()

    # Select case where only one name is chosen
    if isinstance(chosen_names, str):
        chosen_names = [chosen_names]

    for name in chosen_names:
        baby_data = SCOTLAND_DATA[SCOTLAND_DATA['Name'].eq(name)]

        traces.append(
            go.Scatter(
                x=baby_data['Year'],
                y=baby_data['Total'],
                name=name,
            )
        )

    return {
        'data': traces,
        'layout': STANDARD_LAYOUT
    }

if __name__ == '__main__':
    app.run_server(debug=True)
