from util.db import conectar
from datetime import datetime, timedelta
from control.contas_receber_controller import criar_conta_receber

def salvar_venda(data, cliente_id, tipo_cliente, total, desconto, forma_pagamento, observacoes, operador):
    """
    Salva a venda principal na tabela de vendas e retorna o ID gerado.
    Se for uma forma de pagamento a prazo, cria automaticamente a conta a receber.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO vendas (
            data, cliente_id, tipo_cliente, total, desconto,
            forma_pagamento, observacoes, status, operador
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 'pendente', ?)
    ''', (data, cliente_id, tipo_cliente, total, desconto, forma_pagamento, observacoes, operador))

    venda_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Geração automática de conta a receber
    formas_a_prazo = ["boleto", "carteira", "fiado"]
    if forma_pagamento.lower() in formas_a_prazo:
        vencimento = (datetime.strptime(data, "%Y-%m-%d %H:%M:%S") + timedelta(days=30)).strftime("%Y-%m-%d")
        criar_conta_receber(venda_id, cliente_id, total, vencimento, forma_pagamento)

    return venda_id

def salvar_item_venda(venda_id, produto_id, quantidade, preco_unitario, subtotal):
    """
    Salva um item (produto vendido) relacionado à venda.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO itens_venda (
            venda_id, produto_id, quantidade, preco_unitario, subtotal
        )
        VALUES (?, ?, ?, ?, ?)
    ''', (venda_id, produto_id, quantidade, preco_unitario, subtotal))

    conn.commit()
    conn.close()

def listar_vendas():
    """
    Retorna uma lista das vendas registradas.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, data, cliente_id, tipo_cliente, total, desconto, forma_pagamento, status, operador
        FROM vendas
        ORDER BY data DESC
    ''')

    vendas = cursor.fetchall()
    conn.close()
    return vendas

def finalizar_venda(venda_id):
    """
    Atualiza o status da venda para 'finalizada'.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE vendas
        SET status = 'finalizada'
        WHERE id = ?
    ''', (venda_id,))
    conn.commit()
    conn.close()

def listar_itens_venda(venda_id):
    """
    Lista os itens vendidos em uma venda específica.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.nome, iv.quantidade, iv.preco_unitario, iv.subtotal
        FROM itens_venda iv
        JOIN produtos p ON iv.produto_id = p.id
        WHERE iv.venda_id = ?
    ''', (venda_id,))

    itens = cursor.fetchall()
    conn.close()
    return itens

def detalhar_venda(venda_id):
    """
    Retorna os dados gerais da venda e os itens vendidos.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT desconto, total, forma_pagamento
        FROM vendas
        WHERE id = ?
    ''', (venda_id,))
    venda = cursor.fetchone()

    cursor.execute('''
        SELECT p.nome, iv.quantidade, iv.preco_unitario, iv.subtotal, iv.produto_id
        FROM itens_venda iv
        JOIN produtos p ON iv.produto_id = p.id
        WHERE iv.venda_id = ?
    ''', (venda_id,))
    itens = cursor.fetchall()

    conn.close()
    return venda, itens
