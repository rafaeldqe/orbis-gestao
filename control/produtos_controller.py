import sqlite3
from util.db import conectar

def salvar_produto(nome, descricao, preco_custo, preco_venda, quantidade, unidade, estoque_minimo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO produtos (nome, descricao, preco_custo, preco, estoque, unidade, estoque_minimo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nome, descricao, preco_custo, preco_venda, quantidade, unidade, estoque_minimo))
    conn.commit()
    conn.close()

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, nome, descricao, preco_custo, preco, estoque, unidade, estoque_minimo
        FROM produtos
        WHERE ativo = 1
        ORDER BY nome ASC
    ''')
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def buscar_produto_por_id(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, nome, descricao, preco_custo, preco, estoque, unidade, estoque_minimo
        FROM produtos
        WHERE id = ?
    ''', (produto_id,))
    produto = cursor.fetchone()
    conn.close()
    return produto

def atualizar_produto(produto_id, nome, descricao, preco_custo, preco_venda, quantidade, unidade, estoque_minimo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE produtos
        SET nome = ?, descricao = ?, preco_custo = ?, preco = ?, estoque = ?, unidade = ?, estoque_minimo = ?
        WHERE id = ?
    ''', (nome, descricao, preco_custo, preco_venda, quantidade, unidade, estoque_minimo, produto_id))
    conn.commit()
    conn.close()

def contar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM produtos WHERE ativo = 1")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def listar_estoque_baixo():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, nome, estoque, estoque_minimo
        FROM produtos
        WHERE ativo = 1 AND estoque < estoque_minimo
    ''')
    resultado = cursor.fetchall()
    conn.close()
    return resultado
def registrar_movimentacao(produto_id, tipo, quantidade, observacao):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao)
        VALUES (?, ?, ?, ?)
    ''', (produto_id, tipo, quantidade, observacao))

    if tipo == 'saida':
        cursor.execute('UPDATE produtos SET estoque = estoque - ? WHERE id = ?', (quantidade, produto_id))
    elif tipo == 'entrada':
        cursor.execute('UPDATE produtos SET estoque = estoque + ? WHERE id = ?', (quantidade, produto_id))

    conn.commit()
    conn.close()


def baixar_estoque(produto_id, quantidade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE produtos
        SET estoque = estoque - ?
        WHERE id = ?
    ''', (quantidade, produto_id))
    conn.commit()
    conn.close()
