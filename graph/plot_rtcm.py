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

#external_stylesheets = ['']

app = DjangoDash('test')

datepicker =    dcc.DatePickerSingle(
                    id='my-date-picker-single',
                    min_date_allowed=dt(2018, 11, 12),
                    max_date_allowed=dt(2018, 12, 8),
                    initial_visible_month=dt(2018, 11, 1),
                    className='col-2 my_input',
                    style= {
                            'margin-top':'40px',
                            'margin-bottom':'10px',
                        }
                )

inputhour = html.Div(dcc.Input(
                id='chosen-hour',
                placeholder='Hour from 0 to 23',
                type='number',
                min = 0,
                max = 23,
                style={'height':'48px',
                       'width':'160px',
                       'border-style':'ridge',
                       'border-width':'2px',
                       'margin-top':'40px',
                       'margin-bottom':'10px',
                       'background-color':'transparent',
                       'color':'white',
                       'font-size': '1rem',
                       'font-weight':'bold',
                       
                },
            ), className='col-2 my_input')

graph1 = dcc.Graph(id='graph-rtcm', className='col-6')

inputlocation = html.Div(dcc.Input(
                    id='chosen-location',
                    placeholder='Type location',
                    type='text',
                    style={'height':'48px',
                       'width':'150px',
                       'border-style':'ridge',
                       'border-width':'2px',
                       'margin-top':'40px',
                       'margin-bottom':'10px',
                       'background-color':'transparent',
                       'color':'white',
                       'font-size': '1rem',
                       'font-weight':'bold',
                       },
                ), className='col-2 offset-4 my_input')

#output_location = html.Div(id='output-chosen-location')

graph2 = dcc.Graph(id='depth-analyze', className='col-6',)

graph_map = dcc.Graph(id='graph_map', className='col-12 mt-5', style={'margin-top':'20px'})

app.layout = html.Div([
                       datepicker,
                       inputhour,
                       inputlocation,
                       graph1,
                       graph2,
                       graph_map,
                       ],className="row"
                    )

@app.callback(
    Output('graph_map', 'figure'),
    [Input('my-date-picker-single', 'date'),
    Input('chosen-hour', 'value')])

def update_map(date, value):
    traces = []
    traces.append(go.Scattergeo(mode='markers+text',
                                lon= [
                                    
                                ],
                                lat= [
                                    
                                ],
                                marker= {
                                    'size': 7,
                                    'color': ['#bebada', '#fdb462', '#fb8072', '#d9d9d9', '#bc80bd', '#b3de69', '#8dd3c7', '#80b1d3', '#fccde5', '#ffffb3'],
                                    'line': {'width': 1},
                                    },
                                name='Canadian cities',
                                textposition= [
                                    'top right', 'top left', 'top center', 'bottom right', 'top right',
                                    'top left', 'bottom right', 'bottom left', 'top right', 'top right'
                                ],))
    layout= go.Layout(title= 'Belgium',
                      font= {
                            'family': 'Droid Serif, serif',
                            'size': 6,
                        },
                      titlefont= {'size': 16},
                      geo= {'scope': 'europe',
                            'resolution': 50,
                            'lonaxis': {'range': [2, 6]},
                            'lataxis': {'range': [50, 53]},
                            'showrivers': True,
                            'rivercolor': '#fff',
                            'showlakes': True,
                            'lakecolor': '#fff',
                            'showland': True,
                            'landcolor': '#EAEAAE',
                            'countrycolor': '#d3d3d3',
                            'countrywidth': 1.5,
                            'subunitcolor': '#d3d3d3',
                            },)
    return {
            'data': traces,
            'layout': layout}
    

@app.callback(
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
                            plot_bgcolor= 'rgb(0,0,0,0)',
                            paper_bgcolor= 'rgb(0,0,0,0)',
                            font={'color':'white'},
                            #margin={'l': 60, 'b': 40, 't': 10, 'r': 10},
                            #legend={'x': 0, 'y': 1},
                        )
            
    }

@app.callback(
    Output('depth-analyze', 'figure'),
    [Input('chosen-location', 'value'),
     Input('my-date-picker-single', 'date'),
     Input('chosen-hour', 'value')])
def update_output2(loc, date, hour):
    initial_window = 28 #days
    traces = []
    if loc is not None and hour is not None and date is not None:
        from datetime import timedelta
        hour = str(hour)+':00:00'
        end = pd.Timestamp(date + ' ' + hour)
        end2 = end + timedelta(days=1)
        start = end - timedelta(days=initial_window)
        filtered_df = df[df['location'] == loc]
        traces.append(go.Scatter(
                x=filtered_df.loc[start:end].index,
                y=filtered_df.loc[start:end]['y'],
                mode='lines',
                opacity=0.7,
                name = 'measured',
                line = {'color': '#512050'}
                ))
        traces.append(go.Scatter(
                x=filtered_df.loc[start:end2].index,
                y=filtered_df.loc[start:end2]['yhat'],
                mode='lines',
                opacity=0.7,
                name = 'prediction',
                line = {'color': 'red'}
                ))
        traces.append(go.Scatter(
                x=filtered_df.loc[start:end2].index,
                y=filtered_df.loc[start:end2]['yhat_upper'],
                mode='lines',
                opacity=0.7,
                name = 'upper bound',
                line = {'color': 'green'},
                ))
        traces.append(go.Scatter(
                x=filtered_df.loc[start:end2].index,
                y=filtered_df.loc[start:end2]['yhat_lower'],
                mode='lines',
                opacity=0.7,
                name = 'lower bound',
                line = {'color': 'green'}
                ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Date'},
            font={'color':'white'},
            yaxis={'title': 'Amount of People'},
            showlegend=False,
            hovermode='closest',
            plot_bgcolor= 'rgb(0,0,0,0)',
            paper_bgcolor= 'rgb(0,0,0,0)',
        )}
