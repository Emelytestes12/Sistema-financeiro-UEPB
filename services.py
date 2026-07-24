import database
from models import Carteira, Gasto, Transferencia

# Arquivo de serviços do sistema financeiro.

# Busca uma carteira específica pelo ID (1 = Poupança, 2 = Gastos)
def obter_carteira(carteira_id: int) -> Carteira | None:
    conn = database.conectar()
    cursor = conn.cursor()

    # Busca a carteira no banco
    cursor.execute(
        "SELECT id, nome, saldo FROM carteiras WHERE id = ?",
        (carteira_id,)
    )

    row = cursor.fetchone()
    conn.close()

    # Se encontrou, retorna o objeto montado; se não, retorna None
    if row:
        return Carteira(
            id_carteira=row[0],
            nome=row[1],
            saldo=row[2]
        )

    return None


# Adiciona grana nas duas carteiras de uma vez só
def adicionar_salario(valor_poupanca: float, valor_gastos: float):
    carteira_poup = obter_carteira(1)
    carteira_gastos = obter_carteira(2)

    # Se não achar as carteiras, trava a execução e avisa
    if carteira_poup is None or carteira_gastos is None:
        raise ValueError("Carteiras não encontradas.")

    conn = database.conectar()
    cursor = conn.cursor()

    # Soma os valores novos aos saldos antigos
    cursor.execute(
        "UPDATE carteiras SET saldo = ? WHERE id = 1",
        (carteira_poup.saldo + valor_poupanca,)
    )

    cursor.execute(
        "UPDATE carteiras SET saldo = ? WHERE id = 2",
        (carteira_gastos.saldo + valor_gastos,)
    )

    # Salva as alterações no arquivo .db e fecha
    conn.commit()
    conn.close()


# Salva uma compra/gasto e já desconta do saldo de gastos
def registrar_gasto(gasto: Gasto):
    conn = database.conectar()
    cursor = conn.cursor()

    # Insere o novo gasto no histórico
    cursor.execute(
        """
        INSERT INTO gastos (nome, descricao, valor)
        VALUES (?, ?, ?)
        """,
        (gasto.nome, gasto.descricao, gasto.valor)
    )

    carteira_gastos = obter_carteira(2)

    if carteira_gastos is None:
        conn.close()
        raise ValueError("Carteira de gastos não encontrada.")

    # Calcula o novo saldo e atualiza no banco
    novo_saldo = carteira_gastos.saldo - gasto.valor

    cursor.execute(
        "UPDATE carteiras SET saldo = ? WHERE id = 2",
        (novo_saldo,)
    )

    conn.commit()
    conn.close()


# Tira grana da Poupança (ID 1) e passa para Gastos (ID 2)
def realizar_transferencia_emergencia(valor: float):
    carteira_poupanca = obter_carteira(1)
    carteira_gastos = obter_carteira(2)

    if carteira_poupanca is None or carteira_gastos is None:
        raise ValueError("Carteiras não encontradas.")

    # Não deixa transferir se a poupança não tiver saldo suficiente
    if carteira_poupanca.saldo < valor:
        raise ValueError("Saldo insuficiente na poupança.")

    conn = database.conectar()
    cursor = conn.cursor()

    # Anota a movimentação no histórico de transferências
    cursor.execute(
        "INSERT INTO transferencias (valor) VALUES (?)",
        (valor,)
    )

    # Recalcula os dois saldos
    saldo_poupanca = carteira_poupanca.saldo - valor
    saldo_gastos = carteira_gastos.saldo + valor

    # Atualiza a poupança e a carteira de gastos no banco
    cursor.execute(
        "UPDATE carteiras SET saldo = ? WHERE id = 1",
        (saldo_poupanca,)
    )

    cursor.execute(
        "UPDATE carteiras SET saldo = ? WHERE id = 2",
        (saldo_gastos,)
    )

    conn.commit()
    conn.close()


# Puxa todos os gastos (do mais recente pro mais antigo) para preencher a tabela
def obter_todos_gastos() -> list[Gasto]:
    conn = database.conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nome, descricao, valor, id, data
        FROM gastos
        ORDER BY data DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    # Converte cada linha do banco em um objeto Gasto
    return [
        Gasto(
            nome=row[0],
            descricao=row[1],
            valor=row[2],
            id_gasto=row[3],
            data=row[4]
        )
        for row in rows
    ]


# Agrupa a soma dos gastos por dia (usado para gerar gráficos)
def obter_gastos_por_dia() -> dict:
    conn = database.conectar()
    cursor = conn.cursor()

    # Soma os valores agrupando pela data (Ex: {"2026-07-14": 120.50})
    cursor.execute("""
        SELECT DATE(data), SUM(valor)
        FROM gastos
        GROUP BY DATE(data)
        ORDER BY DATE(data)
    """)

    rows = cursor.fetchall()
    conn.close()

    return {row[0]: row[1] for row in rows}


# Puxa o histórico de resgates da poupança para preencher a tabela
def obter_historico_transferencias() -> list[Transferencia]:
    conn = database.conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT valor, data, id
        FROM transferencias
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        Transferencia(
            valor=row[0],
            data=row[1],
            id_transf=row[2]
        )
        for row in rows
    ]