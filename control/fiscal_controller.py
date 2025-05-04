import random
import string
from datetime import datetime
import sqlite3
from util.db import conectar

# Simula assinatura do XML (aqui só carrega e retorna o conteúdo)
def simular_assinatura(xml_path):
    with open(xml_path, "r", encoding="utf-8") as f:
        conteudo = f.read()
    # Simula "assinatura" com tag fictícia
    return conteudo.replace("</NFe>", "<Assinado>true</Assinado></NFe>")

# Simula envio para SEFAZ e retorno autorizado
def simular_envio_sefaz(xml_assinado):
    # Gera chave de acesso fake (44 dígitos)
    chave_acesso = "35" + ''.join(random.choices(string.digits, k=42))
    protocolo = ''.join(random.choices(string.digits, k=15))
    return {
        "status": "autorizado",
        "protocolo": protocolo,
        "chave_acesso": chave_acesso
    }

# Integra tudo: assinatura + envio + atualiza banco
def autorizar_nf_e_simulada(venda_id):
    from control.nfe_controller import gerar_xml_nfe  # Importa local para evitar dependência circular

    xml_path = gerar_xml_nfe(venda_id)
    xml_assinado = simular_assinatura(xml_path)
    resposta = simular_envio_sefaz(xml_assinado)

    # Atualiza o banco de dados
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE vendas SET 
            chave_acesso = ?,
            protocolo = ?,
            status_nf = ?
        WHERE id = ?
    """, (resposta["chave_acesso"], resposta["protocolo"], resposta["status"], venda_id))
    conn.commit()
    conn.close()

    return resposta
