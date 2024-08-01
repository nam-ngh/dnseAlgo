import pandas as pd
import plotly.graph_objects as go
from src.stock import Stock

def plot_stock_price(stock: Stock, width: int=1300, height: int=690):
    '''
    Plots historical stock prices, optionally with ema/sma if they are set
    '''
    df = stock.history
    df['time'] = pd.to_datetime(df['time'])
    fig = go.Figure(
        data=[go.Candlestick(
            x=df['time'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Prices'
        )],
    )
    if hasattr(stock, 'sma'):
        for col in stock.sma.columns:
            fig.add_trace(go.Scatter(x=df['time'], y=stock.sma[col], mode='lines', name=col))
    if hasattr(stock, 'ema'):
        for col in stock.ema.columns:
            fig.add_trace(go.Scatter(x=df['time'], y=stock.ema[col], mode='lines', name=col))
        
    s = str(df['time'].min())[:10]
    e = str(df['time'].max())[:10]
    # Customize the layout
    fig.update_layout(
        title=f'{stock.symbol} historical price {s} to {e}',
        xaxis_title='Date',
        yaxis_title='Price',
        height=height, width=width,
        plot_bgcolor='white', xaxis_linecolor='gray'
    )
    fig.update_xaxes(dtick="D1", tickformat="%d")
    return fig

def plot_macd(stock: Stock, width: int=1300, height: int=690):
    '''Plots MACD for specified stock'''
    df = stock.history
    df['time'] = pd.to_datetime(df['time'])
    # plot
    fig = go.Figure()
    for col in ['MACD','signal']:
        fig.add_trace(go.Scatter(
            x=df['time'], y=stock.macd[col],
            mode='lines', name=col, 
            marker=dict(color='rebeccapurple' if col=='signal' else 'orange')
        ))
    fig.add_trace(go.Bar(
        x=df['time'], y=stock.macd['diff'],
        name='Histogram', marker=dict(color='lightgray')
    ))
    fig.add_hline(y=0, line_color='black')

    s = str(df['time'].min())[:10]
    e = str(df['time'].max())[:10]

    fig.update_layout(
        title=f'{stock.symbol} MACD {s} to {e}',
        xaxis_title='Date',
        yaxis_title='',
        height=height, width=width,
        plot_bgcolor='white',
    )
    fig.update_xaxes(dtick="D1", tickformat="%d")
    return fig