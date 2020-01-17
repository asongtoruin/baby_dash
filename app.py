#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go


external_stylesheets = [
    'https://use.fontawesome.com/releases/v5.8.1/css/brands.css',
    'https://use.fontawesome.com/releases/v5.8.1/css/fontawesome.css',
    dbc.themes.LITERA
]

SCOTLAND_DATA = pd.read_csv(
    'https://raw.githubusercontent.com/asongtoruin/dash_data/master'
    '/Baby%20Names/Filtered%20Names%20Scotland.csv'
)

DATA_SOURCE = 'https://www.nrscotland.gov.uk/statistics-and-data/statistics' \
              '/statistics-by-theme/vital-events/names/babies-first-names'

PROJECT_LINK = 'https://github.com/asongtoruin/baby_dash'

STANDARD_LAYOUT = go.Layout(
    xaxis={'range': [1973, 2019], 'fixedrange': True},
    yaxis={
        'title': 'Number of births',
        'rangemode': 'nonnegative',
        'fixedrange': True,
        'automargin': True
    },
    legend={'orientation': 'h', 'xanchor': 'center', 'x': 0.5, 'y': -0.05},
    margin={'l': 50, 'r': 0, 't': 30},
    showlegend=True
)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Scottish Baby Names'
server = app.server
# app.css.append_css('/assets/spacing.css')

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink(
                html.I(className='fab fa-github fa-lg'),
                href=PROJECT_LINK, external_link=True
            )
        ),
        dbc.NavItem(
            dbc.NavLink('Data Source', href=DATA_SOURCE, external_link=True)
        ),
    ],
    brand='Scottish Baby Names',
    brand_href="#",
    sticky="top",
    dark=False
)

body = dbc.Container([
    dbc.Row(dbc.Col([
    html.H3('Overview'),
    html.Div(
        'View information on the number of babies born by name in '
        'Scotland between 1974 and 2018 (only names appearing more than 10 '
        'times in that period are shown)'
    ),
        ])),
    html.H3('One Name by Gender'),
    html.Div(
        'Use this graph to view usage of a name by gender.'
    ),
    dcc.Dropdown(
        id='single-name-chooser',
        options=[{'label': n, 'value': n}
                 for n in sorted(SCOTLAND_DATA['Name'].unique())],
        value='Adam', multi=False
    ),
    dcc.Graph(id='single-name-graph', config={'displaylogo': False})
    ,
    html.H3('Compare Name Totals'),
    html.Div(
        'Use this graph to compare total instances for multiple names. The '
        'graph can show up to 10 different names with unique colours.'
    ),
    dcc.Dropdown(
        id='multiple-name-chooser',
        options=[{'label': n, 'value': n}
                 for n in sorted(SCOTLAND_DATA['Name'].unique())],
        value=['Adam'], multi=True
    ),
    dcc.Graph(id='comparison-graph', config={'displaylogo': False}),
])


app.layout = html.Div(children=[navbar, body])

@app.callback(Output('single-name-graph', 'figure'),
              [Input('single-name-chooser', 'value')])
def one_baby_name(chosen_name):
    baby_data = SCOTLAND_DATA[SCOTLAND_DATA['Name'].eq(chosen_name)]

    traces = [
        go.Scatter(
            x=baby_data['Year'],
            y=baby_data['Assigned Male'],
            name='Assigned Male',
            mode='markers'
        ),
        go.Scatter(
            x=baby_data['Year'],
            y=baby_data['Assigned Female'],
            name='Assigned Female',
            mode='markers'
        )
    ]

    return {
        'data': traces,
        'layout': STANDARD_LAYOUT
    }


@app.callback(Output('comparison-graph', 'figure'),
              [Input('multiple-name-chooser', 'value')])
def multiple_names(chosen_names):
    traces = []
    if not chosen_names:
        return dict()

    for name in chosen_names:
        baby_data = SCOTLAND_DATA[SCOTLAND_DATA['Name'].eq(name)]

        traces.append(
            go.Scatter(
                x=baby_data['Year'],
                y=baby_data['Total'],
                name=name,
                mode='lines'
            )
        )

    return {
        'data': traces,
        'layout': STANDARD_LAYOUT
    }


if __name__ == '__main__':
    app.run_server(debug=True)
