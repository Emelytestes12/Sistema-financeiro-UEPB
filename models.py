## Aqui é o arquivo de modelos, onde vamos definir as classes que representam os dados do nosso sistema financeiro.
## Serve para organizar e estruturar os dados que vamos manipular no sistema, como carteiras, gastos e transferências.

class Carteira:
    def __init__(self, id_carteira, nome, saldo):
        self.id = id_carteira
        self.nome = nome
        self.saldo = saldo

class Gasto:
    def __init__(self, nome, descricao, valor, id_gasto=None, data=None):
        self.id = id_gasto
        self.nome = nome
        self.descricao = descricao
        self.valor = valor
        self.data = data

class Transferencia:
    def __init__(self, valor, data=None, id_transf=None):
        self.id = id_transf
        self.valor = valor
        self.data = data