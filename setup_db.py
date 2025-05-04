import sqlite3

def atualizar_tabela_produtos():
    try:
        conn = sqlite3.connect("C:/Meus Projetos/orbis_gestao.db")
        cursor = conn.cursor()

        # Adiciona os novos campos se ainda não existirem
        colunas = [row[1] for row in cursor.execute("PRAGMA table_info(produtos);").fetchall()]

        if 'descricao' not in colunas:
            cursor.execute("ALTER TABLE produtos ADD COLUMN descricao TEXT;")
            print("[OK] Campo 'descricao' adicionado.")

        if 'preco_custo' not in colunas:
            cursor.execute("ALTER TABLE produtos ADD COLUMN preco_custo REAL;")
            print("[OK] Campo 'preco_custo' adicionado.")

        if 'unidade' not in colunas:
            cursor.execute("ALTER TABLE produtos ADD COLUMN unidade TEXT DEFAULT 'un';")
            print("[OK] Campo 'unidade' adicionado.")

        if 'estoque_minimo' not in colunas:
            cursor.execute("ALTER TABLE produtos ADD COLUMN estoque_minimo INTEGER DEFAULT 0;")
            print("[OK] Campo 'estoque_minimo' adicionado.")

        conn.commit()
        print("✅ Alterações concluídas com sucesso.")

    except Exception as e:
        print(f"[ERRO] Ocorreu um erro: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    atualizar_tabela_produtos()
