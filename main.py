import tkinter as tk
import database
from gui import AppFinanceiro

##Aqui é o arquivo principal do nosso sistema financeiro, onde vamos inicializar o banco de dados e a interface gráfica.
## Aperta no botão play para rodar o sistema, e o banco de dados vai ser criado automaticamente, sem precisar de nuvem, tudo localmente.
if __name__ == "__main__":
    # 1. Inicializa o banco offline (localmente, sem custos de nuvem)
    database.inicializar_banco()

    # 2. Inicializa a Interface Gráfica (Desktop)
    root = tk.Tk()
    app = AppFinanceiro(root)
    root.mainloop()
