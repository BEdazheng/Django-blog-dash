import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc


df = pd.read_csv('12 november to 8 december.csv')
df['ds'] = pd.to_datetime(df['ds'])
df.set_index('ds', drop=False, inplace=True)
df.columns = ['ds', 'yhat',	'yhat_lower', 'yhat_upper', 'y',
              'anomaly','location','pred_date', 'indicator']

app = DjangoDash('test',
                 meta_tags=[
                         {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ]
        )

app.layout = html.Div([dbc.Col(
    dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=dt(2018, 11, 12),
        max_date_allowed=dt(2018, 12, 8),
        initial_visible_month=dt(2018, 11, 1),
    )),
    dbc.Col(
    dcc.Input(
        id='chosen-hour',
        placeholder='Hour from 0 to 23',
        type='number',
        min = 0,
        max = 23,
        style={'height':'40px', 'width':'150px'},
        )),
    #html.Div(id='output-chosen-ts'),
    dcc.Graph(id='graph-rtcm'),
])

@app.callback(
    #Output('output-chosen-ts', 'children'),
     Output('graph-rtcm', 'figure'),
    [Input('my-date-picker-single', 'date'),
     Input('chosen-hour', 'value')])
def update_output(date, value):
    traces = []
    if date is not None and value is not None:
        value = str(value)+':00:00'
        date = date + ' ' + value
        filtered_df = df.loc[pd.Timestamp(date)].sort_values('anomaly', ascending=False)[:5]
        traces.append(go.Bar(
                x=filtered_df['location'].values,
                y=filtered_df['anomaly'].values,
                name='Test',
# =============================================================================
#                 marker=go.bar.Marker(
#                     color='rgb(55, 83, 109)'
#                 )
# =============================================================================
        ))

    return {
            'data': traces,
            'layout':   go.Layout(
                            xaxis={'title': 'Locations'},
                            yaxis={'title': 'Anomaly Score'},
                            hovermode='closest',
                            #legend={'x': 0, 'y': 1},
                        )
            
    }


import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc


df = pd.read_csv('12 november to 8 december.csv')
df['ds'] = pd.to_datetime(df['ds'])
df.set_index('ds', drop=False, inplace=True)
df.columns = ['ds', 'yhat',	'yhat_lower', 'yhat_upper', 'y',
              'anomaly','location','pred_date', 'indicator']

app = DjangoDash('test',
                 meta_tags=[
                         {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ]
        )

datepicker =    dcc.DatePickerSingle(
                    id='my-date-picker-single',
                    min_date_allowed=dt(2018, 11, 12),
                    max_date_allowed=dt(2018, 12, 8),
                    initial_visible_month=dt(2018, 11, 1),
                )

inputhour = dcc.Input(
                id='chosen-hour',
                placeholder='Hour from 0 to 23',
                type='number',
                min = 0,
                max = 23,
                style={'height':'40px', 'width':'150px'},
            )

graph = dcc.Graph(id='graph-rtcm')

app.layout = html.Div([datepicker, inputhour, html.Br(), graph])

@app.callback(
    #Output('output-chosen-ts', 'children'),
     Output('graph-rtcm', 'figure'),
    [Input('my-date-picker-single', 'date'),
     Input('chosen-hour', 'value')])
def update_output(date, value):
    traces = []
    if date is not None and value is not None:
        value = str(value)+':00:00'
        date = date + ' ' + value
        filtered_df = df.loc[pd.Timestamp(date)].sort_values('anomaly', ascending=False)[:5]
        traces.append(go.Bar(
                x=filtered_df['location'].values,
                y=filtered_df['anomaly'].values,
                name='Test',
# =============================================================================
#                 marker=go.bar.Marker(
#                     color='rgb(55, 83, 109)'
#                 )
# =============================================================================
        ))

    return {
            'data': traces,
            'layout':   go.Layout(
                            xaxis={'title': 'Locations'},
                            yaxis={'title': 'Anomaly Score'},
                            hovermode='closest',
                            #legend={'x': 0, 'y': 1},
                        )
            
    }
