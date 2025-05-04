import sqlite3
from util.db import conectar

def salvar_servico(nome, descricao, valor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO servicos (nome, descricao, valor)
        VALUES (?, ?, ?)
    ''', (nome, descricao, valor))
    conn.commit()
    conn.close()

def listar_servicos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, nome, descricao, valor
        FROM servicos
        WHERE ativo = 1
        ORDER BY nome ASC
    ''')
    servicos = cursor.fetchall()
    conn.close()
    return servicos

def buscar_servico_por_id(servico_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, nome, descricao, valor
        FROM servicos
        WHERE id = ?
    ''', (servico_id,))
    servico = cursor.fetchone()
    conn.close()
    return servico

def atualizar_servico(servico_id, nome, descricao, valor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE servicos
        SET nome = ?, descricao = ?, valor = ?
        WHERE id = ?
    ''', (nome, descricao, valor, servico_id))
    conn.commit()
    conn.close()

def desativar_servico(servico_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE servicos SET ativo = 0 WHERE id = ?
    ''', (servico_id,))
    conn.commit()
    conn.close()