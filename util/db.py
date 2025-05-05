import sqlite3

def conectar():
    return sqlite3.connect("C:/Meus Projetos/orbis/orbis_gestao.db")
