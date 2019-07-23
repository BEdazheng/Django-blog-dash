import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go


df = pd.read_csv('12 november to 8 december.csv')
df['ds'] = pd.to_datetime(df['ds'])
df.set_index('ds', drop=False, inplace=True)
df.columns = ['ds', 'yhat',	'yhat_lower', 'yhat_upper', 'y',
              'anomaly','location','pred_date', 'indicator']

app = DjangoDash('SimpleExample')

app.layout = html.Div([
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=dt(2018, 11, 12),
        max_date_allowed=dt(2018, 12, 8),
        initial_visible_month=dt(2018, 11, 1),
        #end_date=dt(2018, 12, 8),
        calendar_orientation='horizontal',
    ),
    html.Div(id='output-container-date-picker-range'),
    html.Br(),
    dcc.Graph(id='graph-with-slider'),
])

@app.callback(
    Output('output-container-date-picker-range', 'children'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select the date window'
    else:
        return string_prefix

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_figure(start_date, end_date):
    traces = []
    if start_date is not None and end_date is not None:
        filtered_df = df.loc[pd.Timestamp(start_date):pd.Timestamp(end_date)]
        for i in filtered_df.location.unique():
            df_by_index = filtered_df[filtered_df['location'] == i]
            traces.append(go.Scatter(
                x=df_by_index.index,#[j for j in range(df_by_index.shape[0])],
                y=df_by_index['anomaly'],
                #text=df_by_index['location']
                mode='lines',
                opacity=0.7,
                name = i
                )
            )
    #print(list(df_by_index.index))
    return {
    'data': traces,
    'layout': go.Layout(
        xaxis={'title': 'Date'},
        yaxis={'title': 'Anomaly Score', 'range': [0, 15]},
        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
        legend={'x': 0, 'y': 1},
        showlegend=False,
        hovermode='closest',
        plot_bgcolor= 'rgb(0,0,0,0)',
        paper_bgcolor= 'rgb(0,0,0,0)',
        font={'color':'white'},
    )}
        