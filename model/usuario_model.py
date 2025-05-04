from model.conexao import conectar

def criar_tabela_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT DEFAULT 'comum',
            ativo INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

def inserir_usuario(nome, usuario, senha, tipo='admin'):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO usuarios (nome, usuario, senha, tipo, ativo)
        VALUES (?, ?, ?, ?, 1)
    """, (nome, usuario, senha, tipo))
    conn.commit()
    conn.close()

def validar_login(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nome, tipo FROM usuarios WHERE usuario=? AND senha=? AND ativo=1
    """, (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def listar_todos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, usuario, tipo, ativo FROM usuarios")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def editar_usuario(id, nome, usuario, tipo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios SET nome=?, usuario=?, tipo=? WHERE id=?
    """, (nome, usuario, tipo, id))
    conn.commit()
    conn.close()

def desativar_usuario(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuarios SET ativo=0 WHERE id=?
    """, (id,))
    conn.commit()
    conn.close()
