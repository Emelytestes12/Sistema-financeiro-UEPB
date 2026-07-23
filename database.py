import sqlite3  ##Aqui é o nosso banco, vai criar um arquivo chamado financeiro.db localmente, sem precisar de nuvem, e vai armazenar os dados do nosso sistema financeiro.
#OK

def conectar():
    return sqlite3.connect("financeiro.db")

def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS carteiras (
                        id INTEGER PRIMARY KEY,
                        nome TEXT,
                        saldo REAL)''')

    # ==================== ALTERAÇÃO 1 (INÍCIO) ====================
    # Adicionamos a coluna "data" para conseguir agrupar e mostrar os gastos
    # ao longo do tempo (necessário para o novo gráfico de evolução).
    cursor.execute('''CREATE TABLE IF NOT EXISTS gastos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT,
                        descricao TEXT,
                        valor REAL,
                        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    # ==================== ALTERAÇÃO 1 (FIM) ====================

    cursor.execute('''CREATE TABLE IF NOT EXISTS transferencias (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        valor REAL,
                        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    cursor.execute("INSERT OR IGNORE INTO carteiras (id, nome, saldo) VALUES (1, 'Poupança', 0.0)")
    cursor.execute("INSERT OR IGNORE INTO carteiras (id, nome, saldo) VALUES (2, 'Gastos', 0.0)")

    conn.commit()
    conn.close()
