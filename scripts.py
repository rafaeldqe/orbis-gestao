import sqlite3

caminho_db = "C:/Meus Projetos/Orbis/orbis_gestao.db"

def diagnostico_usuarios(caminho_db):
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()

    print(f"🔍 Banco conectado: {caminho_db}")

    # Verifica se a tabela existe
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='usuarios';
    """)
    if not cursor.fetchone():
        print("❌ A tabela 'usuarios' não existe nesse banco.")
        conn.close()
        return

    # Verifica se há usuários cadastrados
    cursor.execute("SELECT * FROM usuarios;")
    usuarios = cursor.fetchall()

    if not usuarios:
        print("⚠️ Nenhum usuário encontrado!")
        print("➕ Criando usuário admin padrão...")

        cursor.execute("""
            INSERT INTO usuarios (nome, usuario, senha, tipo, ativo)
            VALUES (?, ?, ?, ?, ?)
        """, ("Administrador", "admin", "admin123", "admin", 1))
        conn.commit()
        print("✅ Usuário admin criado com sucesso! (login: admin / senha: admin123)")
    else:
        print("✅ Usuários encontrados:")
        for user in usuarios:
            print(f" - {user[0]} | {user[1]} | {user[2]} | Tipo: {user[4]} | Ativo: {user[5]}")

    conn.close()

# Executa
diagnostico_usuarios(caminho_db)
