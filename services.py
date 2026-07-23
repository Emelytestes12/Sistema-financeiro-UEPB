import database
from models import Carteira, Gasto, Transferencia

# ==========================================================
# Arquivo de serviços do sistema financeiro.
# Responsável por manipular os dados do banco de dados.
# ==========================================================


def obter_carteira(carteira_id: int) -> Carteira | None:
    conn = database.conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nome, saldo FROM carteiras WHERE id = ?",
        (carteira_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return Carteira(
            id_carteira=row[0],
            nome=row[1],
            saldo=row[2]
        )

    return None


def adicionar_salario(valor_poupanca: float, valor_gastos: float):
    carteira_poup = obter_carteira(1)
    carteira_gastos = obter_carteira(2)

    # Verifica se as carteiras existem
    if carteira_poup is None or carteira_gastos is None:
        raise ValueError("Carteiras não encontradas.")

    conn = database.conectar()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE carteiras SET saldo = ? WHERE id = 1",
        (carteira_poup.saldo + valor_poupanca,)
    )

    cursor.execute(
        "UPDATE carteiras SET saldo = ? WHERE id = 2",
        (carteira_gastos.saldo + valor_gastos,)
    )

    conn.commit()
    conn.close()


def registrar_gasto(gasto: Gasto):
    conn = database.conectar()
    cursor = conn.cursor()

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

    novo_saldo = carteira_gastos.saldo - gasto.valor

    cursor.execute(
        "UPDATE carteiras SET saldo = ? WHERE id = 2",
        (novo_saldo,)
    )

    conn.commit()
    conn.close()


def realizar_transferencia_emergencia(valor: float):
    carteira_poupanca = obter_carteira(1)
    carteira_gastos = obter_carteira(2)

    if carteira_poupanca is None or carteira_gastos is None:
        raise ValueError("Carteiras não encontradas.")

    # Impede saldo negativo
    if carteira_poupanca.saldo < valor:
        raise ValueError("Saldo insuficiente na poupança.")

    conn = database.conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transferencias (valor) VALUES (?)",
        (valor,)
    )

    saldo_poupanca = carteira_poupanca.saldo - valor
    saldo_gastos = carteira_gastos.saldo + valor

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


def obter_gastos_por_dia() -> dict:
    """
    Retorna um dicionário no formato:
    {
        "2026-07-14": 120.50,
        "2026-07-15": 45.00
    }
    """

    conn = database.conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DATE(data), SUM(valor)
        FROM gastos
        GROUP BY DATE(data)
        ORDER BY DATE(data)
    """)

    rows = cursor.fetchall()
    conn.close()

    return {row[0]: row[1] for row in rows}


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