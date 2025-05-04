from model.conexao import conectar

def criar_tabela_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            codigo TEXT UNIQUE,
            preco REAL NOT NULL,
            estoque INTEGER DEFAULT 0,
            ativo INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, codigo, preco, estoque, ativo FROM produtos
    """)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def inserir_produto(nome, preco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM produtos")
    ultimo_id = cursor.fetchone()[0]
    novo_id = (ultimo_id or 0) + 1
    codigo = f"PROD-{novo_id:03d}"
    cursor.execute("""
        INSERT INTO produtos (nome, codigo, preco, estoque, ativo)
        VALUES (?, ?, ?, 0, 1)
    """, (nome, codigo, preco))
    conn.commit()
    conn.close()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (nome, codigo, preco, estoque, ativo)
        VALUES (?, ?, ?, 0, 1)
    """, (nome, codigo, preco))
    conn.commit()
    conn.close()

def editar_produto(id, nome, codigo, preco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produtos SET nome=?, codigo=?, preco=? WHERE id=?
    """, (nome, codigo, preco, id))
    conn.commit()
    conn.close()

def desativar_produto(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produtos SET ativo=0 WHERE id=?
    """, (id,))
    conn.commit()
    conn.close()

def atualizar_estoque(produto_id, tipo, quantidade):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT estoque FROM produtos WHERE id=?", (produto_id,))
    atual = cursor.fetchone()[0]

    if tipo == 'entrada':
        novo_estoque = atual + quantidade
    elif tipo == 'saida':
        if atual < quantidade:
            raise ValueError("Estoque insuficiente")
        novo_estoque = atual - quantidade

    cursor.execute("UPDATE produtos SET estoque=? WHERE id=?", (novo_estoque, produto_id))
    conn.commit()
    conn.close()
