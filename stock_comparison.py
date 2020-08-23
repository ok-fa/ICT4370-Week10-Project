'''
Author: Fabio Okubo
Date: 8/22/2020
version: 1
Description:
    Graphs two different ticket symbols from YFinance data and using Bokeh
'''

import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import date, datetime
from bokeh.plotting import figure, output_file, show


def get_start_date():
    '''
    Prompts user to enter start date for stock analysis
    '''
    while True:
        try:
            start_date = input("Enter state date in the following format YYYY-MM-DD: ")
            start = datetime.strptime(start_date, '%Y-%m-%d').date()  
            return start
        except:
            print("Invalid date, please try again.")

def add_stock_to_list(message, stocks, start):
    '''
    Prompts uder to enter ticket symbol, loads data to list, add ticket column to data frame
    '''    
    yf.pdr_override()

    now = date.today()

    while True:
        ticker = input(message).upper()
        try:
            df = pdr.get_data_yahoo(ticker, start, now)
            df["Symbol"] = ticker
            stocks.append(df)
            break
        except:
            print("Please try again, symbol not found.")


def graph_adj_close(stocks):
    #create dataframe
    df = pd.DataFrame(stocks[0])
    #yFinance stock data index are the dates
    x_data = df.index
    #get adjusted clock data
    stock1 = df["Adj Close"]
    #since yFinance data is index by date, need to get stock symbol from df based on index
    index = df.index[0]
    symbol1 = df["Symbol"][index]
    df = pd.DataFrame(stocks[1])
    stock2 = df["Adj Close"]
    symbol2 = df["Symbol"][index]

    # output to static HTML file
    output_file("stock_chart.html")

    # create a new plot
    p = figure(x_axis_type="datetime", title="Stock Comparison", plot_height=350, plot_width=800)

    # add some renderers
    p.xgrid.grid_line_color=None
    p.ygrid.grid_line_alpha=0.5
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Adj Close'

    p.line(x_data, stock1, line_width = 2, legend_label = symbol1)
    p.line(x_data, stock2, line_width = 2, color='#cf3c4d', legend_label = symbol2)
    show(p)


def compare_tickers():
    ''' this is the main function in this module'''
    stocks = []

    start_date = get_start_date()
    add_stock_to_list("Enter first ticker symbol: ", stocks, start_date)
    add_stock_to_list("Enter second ticker symbol: ", stocks, start_date)

    graph_adj_close(stocks)
