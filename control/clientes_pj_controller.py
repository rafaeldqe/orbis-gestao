import sqlite3
from util.db import conectar

def salvar_cliente(razao_social, nome_fantasia, cnpj, email, telefone, cep, logradouro, numero, bairro, cidade, estado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clientes_pj (razao_social, nome_fantasia, cnpj, email, telefone, cep, logradouro, numero, bairro, cidade, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (razao_social, nome_fantasia, cnpj, email, telefone, cep, logradouro, numero, bairro, cidade, estado))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, razao_social, nome_fantasia, cnpj, email, telefone, cidade, estado
        FROM clientes_pj
        WHERE ativo = 1
        ORDER BY razao_social ASC
    ''')
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def buscar_cliente_por_id(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM clientes_pj WHERE id = ?
    ''', (cliente_id,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente

def atualizar_cliente(cliente_id, razao_social, nome_fantasia, cnpj, email, telefone, cep, logradouro, numero, bairro, cidade, estado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clientes_pj
        SET razao_social = ?, nome_fantasia = ?, cnpj = ?, email = ?, telefone = ?, cep = ?, logradouro = ?, numero = ?, bairro = ?, cidade = ?, estado = ?
        WHERE id = ?
    ''', (razao_social, nome_fantasia, cnpj, email, telefone, cep, logradouro, numero, bairro, cidade, estado, cliente_id))
    conn.commit()
    conn.close()

def desativar_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clientes_pj SET ativo = 0 WHERE id = ?
    ''', (cliente_id,))
    conn.commit()
    conn.close()
