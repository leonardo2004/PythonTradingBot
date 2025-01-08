import yfinance as yf
import backtrader as bt

tickerName = "ITUB3F.SA"                                     # Seleciona o ticker a ser baixado
data = yf.download(tickerName, period='1d', interval='1m')  # Baixa o ticker e salva em uma dataframe chamada data
data.to_csv(tickerName+'.csv')                              # Salva o arquivo