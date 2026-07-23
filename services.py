import database
from models import Carteira, Gasto, Transferencia

## Aqui é o arquivo de serviços, onde vamos definir as funções que vão manipular os dados do nosso sistema financeiro.
## Como as transferências, os gastos e os saldos das carteiras. Essas funções vão interagir com o banco de dados e com os modelos definidos em models.py.

def obter_carteira(carteira_id) -> Carteira:
    conn = database.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, saldo FROM carteiras WHERE id = ?", (carteira_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Carteira(id_carteira=row[0], nome=row[1], saldo=row[2])
    return None

def adicionar_salario(valor_poupanca, valor_gastos):
    carteira_poup = obter_carteira(1)
    carteira_gastos = obter_carteira(2)

    conn = database.conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE carteiras SET saldo = ? WHERE id = 1", (carteira_poup.saldo + valor_poupanca,))
    cursor.execute("UPDATE carteiras SET saldo = ? WHERE id = 2", (carteira_gastos.saldo + valor_gastos,))
    conn.commit()
    conn.close()

def registrar_gasto(gasto: Gasto):
    conn = database.conectar()
    cursor = conn.cursor()

    # Salva o gasto no banco (a coluna "data" é preenchida automaticamente
    # pelo banco com CURRENT_TIMESTAMP, não precisamos passar valor aqui)
    cursor.execute("INSERT INTO gastos (nome, descricao, valor) VALUES (?, ?, ?)",
                   (gasto.nome, gasto.descricao, gasto.valor))

    # Deduz da carteira de gastos
    carteira_gastos = obter_carteira(2)
    novo_saldo = carteira_gastos.saldo - gasto.valor
    cursor.execute("UPDATE carteiras SET saldo = ? WHERE id = 2", (novo_saldo,))

    conn.commit()
    conn.close()

def realizar_transferencia_emergencia(valor):
    conn = database.conectar()
    cursor = conn.cursor()

    # Registra a transferência
    cursor.execute("INSERT INTO transferencias (valor) VALUES (?)", (valor,))

    # Atualiza as carteiras
    saldo_poupanca = obter_carteira(1).saldo - valor
    saldo_gastos = obter_carteira(2).saldo + valor

    cursor.execute("UPDATE carteiras SET saldo = ? WHERE id = 1", (saldo_poupanca,))
    cursor.execute("UPDATE carteiras SET saldo = ? WHERE id = 2", (saldo_gastos,))

    conn.commit()
    conn.close()

# ==================== ALTERAÇÃO 3 (INÍCIO) ==================== oK
def obter_todos_gastos() -> list[Gasto]:
    conn = database.conectar()
    cursor = conn.cursor()
    # Agora também buscamos a coluna "data" e ordenamos do mais recente
    # para o mais antigo, para a lista fazer mais sentido pro usuário.
    cursor.execute("SELECT nome, descricao, valor, id, data FROM gastos ORDER BY data DESC")
    rows = cursor.fetchall()
    conn.close()
    return [Gasto(nome=row[0], descricao=row[1], valor=row[2], id_gasto=row[3], data=row[4]) for row in rows]
# ==================== ALTERAÇÃO 3 (FIM) ====================


# ==================== ALTERAÇÃO 4 (INÍCIO) - FUNÇÃO NOVA ==================== #OK
def obter_gastos_por_dia() -> dict:
    """
    Agrupa o total de gastos por dia (ignorando a hora).
    Usado para gerar o gráfico de evolução de gastos ao longo do tempo.
    Retorna um dicionário no formato {"2026-07-14": 120.50, "2026-07-15": 45.00}
    """
    conn = database.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT date(data) as dia, SUM(valor) FROM gastos GROUP BY dia ORDER BY dia")
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}
# ==================== ALTERAÇÃO 4 (FIM) - FUNÇÃO NOVA ====================

def obter_historico_transferencias() -> list[Transferencia]:
    conn = database.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT valor, data, id FROM transferencias ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [Transferencia(valor=row[0], data=row[1], id_transf=row[2]) for row in rows]
