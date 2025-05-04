from model.conexao import conectar
from model.produto_model import atualizar_estoque

def criar_tabela_movimentacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            tipo TEXT CHECK(tipo IN ('entrada', 'saida')),
            quantidade INTEGER NOT NULL,
            data TEXT DEFAULT CURRENT_TIMESTAMP,
            observacao TEXT,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    """)
    conn.commit()
    conn.close()

def registrar_movimentacao(produto_id, tipo, quantidade, observacao=""):
    atualizar_estoque(produto_id, tipo, quantidade)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao)
        VALUES (?, ?, ?, ?)
    """, (produto_id, tipo, quantidade, observacao))
    conn.commit()
    conn.close()
