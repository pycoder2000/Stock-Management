import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import date, datetime
import pandas_datareader.data as web
from django_plotly_dash import DjangoDash

# File contains Stock tickers for all NASDAQ symbols
nasdaq = pd.read_csv('data/NASDAQcompanylist.csv')

# Plotly Dash App applied within Django

app = DjangoDash('stock-graphic')

app.layout = html.Div([

    # First row with inputs and button

    html.Div([
        html.H3('Select stock symbols:', style={'paddingRight': '50px'}),
        dcc.Dropdown(id='stock-dropdown',
                     options=[dict(label=ticker, value=ticker) for ticker in nasdaq['Symbol']],
                     multi=True,),
    ], style=dict(display='inline-block',
                  verticalAlign='top',
                  width='40%',)),

    html.Div([
        html.H3('Select date range'),
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=datetime(2015, 1, 1),
            max_date_allowed=datetime.today(),
            minimum_nights=30,
            clearable=True,
            with_portal=True,
            start_date=date(2016, 1, 1),
            end_date=datetime.today()
        )], style={'display':'inline-block', 'marginLeft': '30px'}),

    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize': 20, 'marginLeft': '30px'}
        ),
    ], style={'display': 'inline-block'}),


    # Second row contains share graphic only

    html.Div(
        dcc.Graph(id='display-graphic',
                  figure=dict(data=[dict(x=[0, 1],
                                         y=[0, 1])],
                              layout=dict(
                                  height=500,
                                  # title='Default',
                                  markers='closest')
                              ))
    )
])


@app.callback(Output('display-graphic', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('stock-dropdown', 'value'),
               State('date-range', 'start_date'),
               State('date-range', 'end_date')])
def update_graph(n_clicks, ticker, start_date, end_date):

    """Retrieves stock price history for all tickers from Yahoo using the Pandas module."""

    data = []
    graph_title = "Stocks: "

    for tick in ticker:
        graph_title = graph_title + tick + ", "
        df = (web.DataReader(tick,
                             start=start_date,
                            end=end_date,
                            data_source='yahoo'))

        data.append(dict(x=df.index,
                          y=df['Close'],
                         name=tick))

    graph_title = graph_title[:-2]

    figure = dict(data=data,
                  layout=dict(title=f"{graph_title}"))
    return figure
