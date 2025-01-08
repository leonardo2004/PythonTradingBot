import backtrader as bt

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):                                             # Inicializa a classe
        self.dataclose = self.datas[0].close                        # Salva o fechamento na posição [0] da dataseries
        self.order = None                                           # Cria uma variável pra salvar as ordens pendentes



    def notify_order(self, order):

        if order.status in [order.Submitted, order.Accepted]:                   # Se a ordem foi submetida ou aceita,
            return                                                              # não faz nada

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:    # Se a ordem foi cancelada, margem
            self.log('Ordem Cancelada/Margem/Rejeitada')                          # ou rejeitada, mostra um log avisando
        
        if order.status in [order.Completed]:                                   # Se a ordem for completa mostra um log
            if order.isbuy():                                                   # caso for ordem de compra ou caso for
                self.log('COMPRA EXECUTADA, %.2f' % order.executed.price)           # ordem de venda
            elif order.issell():                                                #
                self.log('VENDA EXECUTADA, %.2f' % order.executed.price)          # Atenção: Broker pode recusar ordem se
            self.bar_executed = len(self)                                       # não tiver dinheiro o bastante

        self.order = None                                                   # Anotando que não há nenhum pedido pendente



    def next(self):
        # Imprime o preço de fechamento pra referência
        self.log('Fechamento, %.2f' % self.dataclose[0])

        # Verifica se há ordem pendente, se tiver ele não opera
        if self.order:
            return

        # Verifica se não estiver em posição no mercado
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] < self.dataclose[-1]:
                    # current close less than previous close

                    if self.dataclose[-1] < self.dataclose[-2]:
                        # previous close less than the previous close

                        # BUY, BUY, BUY!!! (with default parameters)
                        self.log('ORDEM DE COMPRA, %.2f' % self.dataclose[0])

                        # Keep track of the created order to avoid a 2nd order
                        self.order = self.buy()

        else:

            # Already in the market ... we might sell
            if len(self) >= (self.bar_executed + 5):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('ORDEM DE VENDA, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
