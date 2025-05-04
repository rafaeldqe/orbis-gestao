import sqlite3
from util.db import conectar

def salvar_cliente(nome, cpf, email, telefone, cep, logradouro, numero, bairro, cidade, estado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clientes_pf (nome, cpf, email, telefone, cep, logradouro, numero, bairro, cidade, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, cpf, email, telefone, cep, logradouro, numero, bairro, cidade, estado))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, nome, cpf, email, telefone, cidade, estado
        FROM clientes_pf
        WHERE ativo = 1
        ORDER BY nome ASC
    ''')
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def buscar_cliente_por_id(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM clientes_pf WHERE id = ?
    ''', (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente

def atualizar_cliente(cliente_id, nome, cpf, email, telefone, cep, logradouro, numero, bairro, cidade, estado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clientes_pf
        SET nome = ?, cpf = ?, email = ?, telefone = ?, cep = ?, logradouro = ?, numero = ?, bairro = ?, cidade = ?, estado = ?
        WHERE id = ?
    ''', (nome, cpf, email, telefone, cep, logradouro, numero, bairro, cidade, estado, cliente_id))
    conn.commit()
    conn.close()

def desativar_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clientes_pf SET ativo = 0 WHERE id = ?
    ''', (cliente_id,))
    conn.commit()
    conn.close()
