from util.db import conectar
from datetime import datetime

def inserir_conta_receber(venda_id, cliente_id, valor_total, vencimento, forma_pagamento):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contas_receber (venda_id, cliente_id, valor_total, vencimento, forma_pagamento)
        VALUES (?, ?, ?, ?, ?)
    """, (venda_id, cliente_id, valor_total, vencimento, forma_pagamento))
    conn.commit()
    conn.close()

def listar_contas(status=None):
    conn = conectar()
    cursor = conn.cursor()
    if status:
        cursor.execute("SELECT * FROM contas_receber WHERE status = ? ORDER BY vencimento ASC", (status,))
    else:
        cursor.execute("SELECT * FROM contas_receber ORDER BY vencimento ASC")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def registrar_pagamento(conta_id):
    data_pagamento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE contas_receber
        SET status = 'pago', data_pagamento = ?
        WHERE id = ?
    """, (data_pagamento, conta_id))
    conn.commit()
    conn.close()

def criar_conta_receber(venda_id, cliente_id, valor_total, vencimento, forma_pagamento="boleto"):
    """
    Função compatível com o controller de vendas para geração automática da conta.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contas_receber (venda_id, cliente_id, valor_total, vencimento, forma_pagamento, status)
        VALUES (?, ?, ?, ?, ?, 'pendente')
    """, (venda_id, cliente_id, valor_total, vencimento, forma_pagamento))
    conn.commit()
    conn.close()
