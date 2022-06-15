from matplotlib.axis import XAxis
import psycopg2
import psycopg2.extras
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib
import pandas as pd
import PyQt5
import matplotlib.dates as mdates
import cufflinks as cf
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import iplot, init_notebook_mode

cf.go_offline()
init_notebook_mode()
plt.style.use('ggplot')
matplotlib.use('Qt5Agg')


def convert_format(s: str):
    date = datetime.strptime(s, '%Y/%m/%d').date()
    return date


def daily_close_prices():
    close_prices = []
    dates = []
    cur.execute('SELECT RELEASED_DATE, CLOSE_PRICE FROM USDPRICES')
    results = cur.fetchall()

    for item in results:
        dates.append(convert_format(item[0]))
        close_prices.append(item[1]/10)

    df = pd.DataFrame({'Date': dates, 'Close Price': close_prices})

    fig = px.line(df, x='Date', y='Close Price', hover_data={
                  "Date": "|%B %d, %Y"}, title='Daily Close Price')
    fig.update_xaxes(dtick="M1", tickformat='%Y-%m')
    fig.show()


def candle_stick():
    open_prices = []
    low_prices = []
    high_prices = []
    close_prices = []
    dates = []
    cur.execute(
        'SELECT RELEASED_DATE, OPEN_PRICE, LOW_PRICE, HIGH_PRICE, CLOSE_PRICE FROM USDPRICES')
    results = cur.fetchall()

    for item in results:
        dates.append(convert_format(item[0]))
        open_prices.append(item[1]/10)
        low_prices.append(item[2]/10)
        high_prices.append(item[3]/10)
        close_prices.append(item[4]/10)

    df = pd.DataFrame({'Date': dates, 'Open Price': open_prices, 'Low Price': low_prices,
                      'High Price': high_prices, 'Close Price': close_prices})
    
    # fig = go.Figure(data=[go.Candlestick(x=df['Date'],
    #                                      open=df["Open Price"],
    #                                      high=df["High Price"],
    #                                      low=df["Low Price"],
    #                                      close=df["Close Price"])]
    #                 )

    # fig.update_layout(
    #     title='Daily Candlestick Chart',
    #     yaxis_title="Price",
    #     xaxis_title = 'Date'
    # )
    
    # fig.update_xaxes(dtick="M1", tickformat='%Y-%m')

    # fig.show()
    
    qf = cf.QuantFig(df, title="Apple's stock price in 2021", name='AAPL')
    qf.iplot()


conn = psycopg2.connect(host='localhost', database='data',
                        user='ghazal', password='qwerty')

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# daily_close_prices()
candle_stick()
cur.close()

conn.close()
