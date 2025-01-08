from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime
import os.path
import sys
import backtrader as bt
import matplotlib
from Strategies import TestStrategy

cerebro = bt.Cerebro()                                          # Inicializa o cerebro
modpath = os.path.dirname(os.path.abspath(sys.argv[0]))         # Pega o caminho do arquivo do código
datapath = os.path.join(modpath, 'datas/BTC-USD.csv')           # Define o caminho onde os dados estão

#Importa os dados em .csv, dados encontrados na pasta "datas", definida anteriormente em "datapath"
data = bt.feeds.YahooFinanceCSVData(dataname=datapath)

                                        
cerebro.adddata(data)                   # Adiciona os dados ao cerebro
cerebro.broker.setcash(1000000.0)       # Define o dinheiro inicial da simulação
cerebro.addstrategy(TestStrategy)       # Adiciona a estratégia, essa definida no arquivo "estratégias"
print('Valor inicial do portfólio: %.2f' % cerebro.broker.getvalue()) # Imprime o valor inicial da conta
delta = -(cerebro.broker.getvalue())

cerebro.run()
cerebro.plot()
delta += (cerebro.broker.getvalue())
# Imprime o valor final da conta e a variação que o porfólio teve
print('Valor final do portfólio: %.2f' % cerebro.broker.getvalue() , "\nVariação do porfólio %.2f" % delta) 