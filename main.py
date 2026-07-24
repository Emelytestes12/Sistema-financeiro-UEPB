
import database
from gui import AppFinanceiro

if __name__ == "__main__":
    # 1. Inicializa o banco de dados
    database.inicializar_banco()

    # 2. Inicializa a interface gráfica
    app = AppFinanceiro()
    app.mainloop()