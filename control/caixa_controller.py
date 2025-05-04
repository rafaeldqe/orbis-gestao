import sqlite3
from util.db import conectar
import datetime

def caixa_em_aberto_por_operador(operador):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id
        FROM caixa
        WHERE operador = ? AND status = 'aberto'
    ''', (operador,))
    caixa = cursor.fetchone()
    conn.close()
    return caixa is not None

def buscar_caixa_aberto(operador):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, data_abertura, saldo_inicial
        FROM caixa
        WHERE operador = ? AND status = 'aberto'
    ''', (operador,))
    caixa = cursor.fetchone()
    conn.close()
    return caixa

def abrir_caixa(operador, saldo_inicial):
    data_abertura = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO caixa (data_abertura, saldo_inicial, operador, status)
        VALUES (?, ?, ?, 'aberto')
    ''', (data_abertura, saldo_inicial, operador))
    conn.commit()
    conn.close()

def fechar_caixa(caixa_id, saldo_final):
    """
    Fecha o caixa com o ID informado, salvando o saldo final calculado.
    """
    conn = conectar()
    cursor = conn.cursor()

    data_fechamento = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        UPDATE caixa
        SET data_fechamento = ?, saldo_final = ?, status = 'fechado'
        WHERE id = ?
    ''', (data_fechamento, saldo_final, caixa_id))

    conn.commit()
    linhas_afetadas = cursor.rowcount
    conn.close()

    if linhas_afetadas == 0:
        print(f"⚠️ Nenhum caixa foi fechado (ID não encontrado ou já fechado): {caixa_id}")
    else:
        print(f"✅ Caixa {caixa_id} fechado com sucesso. Saldo final: R$ {saldo_final:.2f}")
