from util.db import conectar

def listar_todos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, usuario, senha, tipo, ativo FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def inserir_usuario(nome, usuario, senha, tipo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios (nome, usuario, senha, tipo, ativo)
        VALUES (?, ?, ?, ?, 1)
    """, (nome, usuario, senha, tipo))
    conn.commit()
    conn.close()

def editar_usuario(id, nome, usuario, tipo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET nome = ?, usuario = ?, tipo = ?
        WHERE id = ?
    """, (nome, usuario, tipo, id))
    conn.commit()
    conn.close()

def desativar_usuario(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET ativo = 0
        WHERE id = ?
    """, (id,))
    conn.commit()
    conn.close()
