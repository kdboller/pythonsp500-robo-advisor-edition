#######
# Python for Finance:  Stock Portfolio Analyses with Plotly Dash, Robo Advisor Edition.
######

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
import plotly.graph_objs as go
from datetime import datetime
import pandas as pd
import numpy as np

app = dash.Dash()

tickers = pd.read_csv('tickers.csv')
tickers.set_index('Ticker', inplace=True)

data_index = pd.read_csv('analyzed_portfolio.csv')

data_summary_index = pd.read_csv('data_summary.csv')

data_divs_only_index = pd.read_csv('analyzed_portfolio_divs_only.csv')

data_index_allocation = pd.read_csv('allocation.csv')

options = []

for tic in tickers.index:
	#{'label': 'user sees', 'value': 'script sees'}
	mydict = {}
	mydict['label'] = tic #Apple Co. AAPL
	mydict['value'] = tic
	options.append(mydict)


app.layout = html.Div([
				html.H1('Position Comparison'),
                dcc.Markdown(''' --- '''), 
                html.H2('Relative Returns Comparison'),
                html.Div([html.H3('Enter a stock symbol:', style={'paddingRight': '30px'}),
                dcc.Dropdown(
                          id='my_ticker_symbol',
                          options = options,
                          value = ['SPY', 'VTI'], 
                          multi = True
                          # style={'fontSize': 24, 'width': 75}
                )

                ], style={'display': 'inline-block', 'verticalAlign':'top', 'width': '30%'}),
                html.Div([html.H3('Enter start / end date:'),
                    dcc.DatePickerRange(id='my_date_picker',
                                        min_date_allowed = datetime(2015,1,1),
                                        max_date_allowed = datetime.today(),
                                        start_date = datetime(2018, 1, 1),
                                        end_date = datetime.today()
                    )

                ], style={'display':'inline-block'}), 
                html.Div([
                    html.Button(id='submit-button',
                                n_clicks = 0,
                                children = 'Submit',
                                style = {'fontSize': 24, 'marginLeft': '30px'}

                    )

                ], style={'display': 'inline-block'}),
                 
                dcc.Graph(id='my_graph',
                            figure={'data':[
                                {'x':[1,2], 'y':[3,1]}

                            ], 'layout':{'title':'Default Title'}}
                ),
                dcc.Markdown(''' --- '''),
                    html.H1('Index Strategy Charts'),
					dcc.Markdown(''' --- '''),
					html.H2('Allocation Charts'),
					dcc.Graph(id='allocation1',
	                                        figure = {'data':[
	                                                go.Bar(
	    											x = data_index_allocation['Ticker'],
	    											y = data_index_allocation['Target_Alloc'],
	    											name = 'Target Allocation'),
	    											go.Bar(
												    x = data_index_allocation['Ticker'],
												    y = data_index_allocation['Allocation'],
												    name = 'Current Allocation')
	                                                ],
	                                        'layout':go.Layout(title='Target Allocation versus Current Allocation',
	                                        					barmode='group', 
	                                                            xaxis = {'title':'Ticker', 'tickformat':".2%"},
	                                                            yaxis = {'title':'Allocations', 'tickformat':".1%"},
	                                                            legend = {'x':'0.8', 'y':'1.2'}
	                                         )}, style={'width': '100%'}
	                                        ),
					dcc.Graph(id='allocation2',
	                                        figure = {'data':[
	                                                go.Bar(
	    											x = data_index_allocation['Ticker'],
	    											y = data_index_allocation['Ticker Share Value'],
	    											name = 'Ticker Share Value ($)'),
	    											go.Scatter(
												    x = data_index_allocation['Ticker'],
												    y = data_index_allocation['Allocation'],
												    yaxis='y2',
												    name = '% Allocation')
	                                                ],
	                                        'layout':go.Layout(title='Total Ticker Share Value and % Allocation',
	                                        					barmode='group', 
	                                                            xaxis = {'title':'Ticker'},
	                                                            yaxis = {'title':'Ticker Share Value ($)', 'tickformat': "$:,.2f"},
	                                                            yaxis2= {'title':'% Allocation', 'overlaying':'y', 'side':'right', 'tickformat':".1%",'range':[0,1]},
	                                                            legend = {'x':'0.8', 'y':'1.2'}
	                                         )}, style={'width': '100%'}
	                                        ),
				dcc.Markdown(''' --- '''),

				# Summary Tables of Stock | ETF Metrics
				html.H2('Summary Tables for Stock | ETF Metrics'),
				 dcc.Graph(id='table_index1',
                                        figure = {'data':[
                                                go.Table(
    											header=dict(values=list(data_summary_index.columns),
                								fill = dict(color='#C2D4FF'),
                								align = ['left'] * 5),
    											cells=dict(values=[data_summary_index['Ticker #'],
							                       data_summary_index['Acquisition Date'],
							                       data_summary_index['Ticker'],
							                       data_summary_index['Unit Cost'],
							                       data_summary_index['Cost Basis'],
							                       data_summary_index['Ticker Adj Close'],
							                       data_summary_index['Ticker Return'],
							                       data_summary_index['SP Return'],
							                       data_summary_index['Stock Gain / (Loss)'],
							                       data_summary_index['Share YTD'],
							                       data_summary_index['Closing High Adj Close'],
							                       data_summary_index['Closing High Adj Close Date'],
							                       data_summary_index['Pct off High'],
							                       data_summary_index['Dividend Amt'],
							                       data_summary_index['Share Yield'],
							                       data_summary_index['Market Yield'],
							                       data_summary_index['Current Yield'],
							                       data_summary_index['Ex-Div. Date'],
							                       data_summary_index['Latest Div Amt']
							                      ],
							               fill = dict(color='#F5F8FF'),
							               align = ['left'] * 5,
							                height = 40))],
                                        'layout':go.Layout(title='Summary Stock Metrics',
                                        					# barmode='group', 
                                                            xaxis = {'title':'Summary'},
                                                            yaxis = {'title':'Metrics'}
                                         )}, style={'width': '100%'}
                                        ),
					dcc.Markdown(''' --- '''),

				# YTD Returns versus S&P 500 section
				html.H2('YTD Returns versus S&P 500'),
				dcc.Graph(id='ytd_index1',
                                        figure = {'data':[
                                                go.Bar(
    											x = data_index['Ticker'],
    											y = data_index['Share YTD'],
    											name = 'Ticker YTD'),
    											go.Scatter(
											    x = data_index['Ticker'],
											    y = data_index['SP 500 YTD'],
											    name = 'SP500 YTD')
                                                ],
                                        'layout':go.Layout(title='YTD Return vs S&P 500 YTD',
                                        					barmode='group', 
                                                            xaxis = {'title':'Ticker'},
                                                            yaxis = {'title':'Returns', 'tickformat':".2%"}
                                         )}, style={'width': '100%'}
                                        ),
				dcc.Markdown(''' --- '''),

				# Total Return Charts section
				html.H2('Total Return Charts'),
					dcc.Graph(id='total_index1',
                                        figure = {'data':[
                                                go.Bar(
    											x = data_index['Ticker #'],
    											y = data_index['Ticker Return'],
    											name = 'Ticker Total Return'),
    											go.Scatter(
											    x = data_index['Ticker #'],
											    y = data_index['SP Return'],
											    name = 'SP500 Total Return')
                                                ],
                                        'layout':go.Layout(title='Total Return vs S&P 500',
                                        					barmode='group', 
                                                            xaxis = {'title':'Ticker'},
                                                            yaxis = {'title':'Returns', 'tickformat':".2%"}
                                         )}, style={'width': '100%'}
                                        ),
					dcc.Markdown(''' --- '''),
				# Total Cumulative Investments Over Time section
				html.H2('Total Cumulative Investments Over Time'),
					dcc.Graph(id='tcot_index1',
                                        figure = {'data':[
                                                go.Scatter(
    											x = data_index['Ticker #'],
    											y = data_index['Cum Invst'],
    											mode = 'lines+markers',
    											name = 'Cum Invst'),
    											go.Scatter(
											    x = data_index['Ticker #'],
											    y = data_index['Cum Ticker Returns'],
											    mode = 'lines+markers',
											    name = 'Cum Ticker Returns'),
											    go.Scatter(
    											x = data_index['Ticker #'],
											    y = data_index['Cum SP Returns'],
											    mode = 'lines+markers',	
											    name = 'Cum SP500 Returns'
											    )
		                                        ],
                                        'layout':go.Layout(title='Cumulative Investment Returns by Ticker',
                                        					barmode='group', 
                                                            xaxis = {'title': 'Ticker'},
                                                            yaxis = {'title': 'Returns'},
                                                            legend = {'x':'1', 'y':'1'}
                                         )}, style={'width': '100%'}
                                        ),
					dcc.Graph(id='tcot_index2',
                                        figure = {'data':[
                                                go.Scatter(
    											x = data_index['Ticker #'],
    											y = data_index['Cum Ticker ROI Pct'],
    											mode = 'lines+markers',
    											name = 'Cum Ticker ROI Pct'),
    											go.Scatter(
											    x = data_index['Ticker #'],
											    y = data_index['Cum SP ROI Pct'],
											    mode = 'lines+markers',
											    name = 'Cum SP ROI Pct'),
		                                        ],
                                        'layout':go.Layout(title='Pct Comparisons by Ticker',
                                        					barmode='group', 
                                                            xaxis = {'title': 'Ticker'},
                                                            yaxis = {'title': 'Returns', 'tickformat':".2%"},
                                                            legend = {'x':'0.8', 'y':'1.2'}
                                         )}, style={'width': '100%'}
                                        ),
					dcc.Markdown(''' --- '''),
					# Current Share Price versus Closing High Since Purchased
					html.H2('Current Share Price versus Closing High Since Purchased'),
					dcc.Graph(id='cvh_index1',
                                        figure = {'data':[
                                                go.Bar(
    											x = data_index['Ticker #'],
    											y = data_index['Pct off High'],
    											name = 'Pct off High'),
    											go.Scatter(
    											x = data_index['Ticker #'],
    											y = [-0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25],
    											mode='lines',
    											name='Trailing Stop Marker',
    											line = {'color':'red'}
    											)
		                                        ],
                                        'layout':go.Layout(title='Adj Close % off of High Since Purchased',
                                        					barmode='group', 
                                                            xaxis = {'title': 'Ticker'},
                                                            yaxis = {'title': '% Below High Since Purchased', 'tickformat':'.2%'},
                                                            legend = {'x':'0.8', 'y':'1.2'}
                                         )}, style={'width': '100%'}
                                        ),
					dcc.Markdown(''' --- '''),
				# Total Stock Dividends and Share Yield
				html.H2('Total Stock Dividends and Share Yield'),
					dcc.Graph(id='totaldiv_index1',
	                                        figure = {'data':[
	                                                go.Bar(
	    											x = data_divs_only_index['Ticker #'],
	    											y = data_divs_only_index['Total Stock Return'],
	    											name = 'Ticker TSR'),
	    											go.Scatter(
												    x = data_divs_only_index['Ticker #'],
												    y = data_divs_only_index['Total SP500 Return'],
												    name = 'SP500 TSR')
	                                                ],
	                                        'layout':go.Layout(title='TSR Comparison, Ticker versus SP500',
	                                        					barmode='group', 
	                                                            xaxis = {'title':'Ticker', 'tickformat':".1%"},
	                                                            yaxis = {'title':'Returns', 'tickformat':".1%"},
	                                                            legend = {'x':'0.8', 'y':'1.2'}
	                                         )}, style={'width': '100%'}
	                                        ),
					dcc.Graph(id='totaldiv_index2',
                                        figure = {'data':[
                                                go.Scatter(
    											x = data_index['Ticker #'],
    											y = data_index['Cum Invst'],
    											mode = 'lines+markers',
    											name = 'Cum Invst'),
    											go.Scatter(
											    x = data_index['Ticker #'],
											    y = data_index['Cum Stock Returns'],
											    mode = 'lines+markers',
											    name = 'Cum Stock Returns'),
											    go.Scatter(
    											x = data_index['Ticker #'],
											    y = data_index['Cum Total SP Returns'],
											    mode = 'lines+markers',	
											    name = 'Cum SP500 Returns'
											    )
		                                        ],
                                        'layout':go.Layout(title='Cumulative TSR Comparisons by Ticker',
                                        					barmode='group', 
                                                            xaxis = {'title': 'Ticker'},
                                                            yaxis = {'title': 'Returns'},
                                                            legend = {'x':'0.8', 'y':'1.2'}
                                         )}, style={'width': '100%'}
                                        ),
					dcc.Graph(id='totaldiv_index3',
                                        figure = {'data':[
                                                go.Scatter(
    											x = data_index['Ticker #'],
    											y = data_index['Cum Ticker Returns Pct'],
    											mode = 'lines+markers',
    											name = 'Cum Ticker Returns Pct'),
    											go.Scatter(
											    x = data_index['Ticker #'],
											    y = data_index['Cum SP Returns Pct'],
											    mode = 'lines+markers',
											    name = 'Cum SP Returns Pct'),
		                                        ],
                                        'layout':go.Layout(title='Cumulative TSR Pct Comparisons by Ticker',
                                        					barmode='group', 
                                                            xaxis = {'title': 'Ticker'},
                                                            yaxis = {'title': 'Returns', 'tickformat':".1%"},
                                                            legend = {'x':'0.8', 'y':'1.2'}
                                         )}, style={'width': '100%'}
                                        )


])

@app.callback(Output('my_graph', 'figure'),
				[Input('submit-button', 'n_clicks')],
				[State('my_ticker_symbol', 'value'),
					  State('my_date_picker', 'start_date'),
					  State('my_date_picker', 'end_date')

				])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
	start = datetime.strptime(start_date[:10], '%Y-%m-%d')
	end = datetime.strptime(end_date[:10], '%Y-%m-%d')

	traces = []
	for tic in stock_ticker:
		df = web.DataReader(tic, 'iex', start, end)
		traces.append({'x':df.index, 'y':(df['close']/df['close'].iloc[0])-1, 'name': tic})
	
	fig = {
		'data': traces,
		'layout': {'title':stock_ticker}
	}
	return fig

if __name__ == '__main__':
    app.run_server()
