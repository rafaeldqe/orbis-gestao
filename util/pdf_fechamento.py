from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from util.db import conectar

def gerar_pdf_fechamento(caixa_id, pasta_destino="fechamentos"):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fechamento_caixa WHERE id = ?", (caixa_id,))
    caixa = cursor.fetchone()
    conn.close()

    if not caixa:
        print("Caixa não encontrado.")
        return

    os.makedirs(pasta_destino, exist_ok=True)
    nome_arquivo = os.path.join(pasta_destino, f"fechamento_caixa_{caixa_id}.pdf")

    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    y = altura - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Relatório de Fechamento de Caixa - Nº {caixa_id}")

    c.setFont("Helvetica", 10)
    y -= 30

    def safe_format(valor):
        return f"R$ {float(valor or 0):.2f}"

    campos = [
        ("Data Abertura", caixa[1]),
        ("Data Fechamento", caixa[2]),
        ("Operador", caixa[3]),
        ("Valor Inicial", safe_format(caixa[4])),
        ("Dinheiro", safe_format(caixa[5])),
        ("Cartão Crédito", safe_format(caixa[6])),
        ("Cartão Débito", safe_format(caixa[7])),
        ("Pix", safe_format(caixa[8])),
        ("Boleto", safe_format(caixa[9])),
        ("Outros", safe_format(caixa[10])),
        ("Saídas", safe_format(caixa[11])),
        ("Valor Contado", safe_format(caixa[12])),
        ("Diferença", safe_format(caixa[13])),
        ("Status", caixa[15]),
    ]

    for campo, valor in campos:
        c.drawString(50, y, f"{campo}: {valor}")
        y -= 20

    # Observações
    y -= 10
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Observações:")
    y -= 20
    c.setFont("Helvetica", 10)

    texto = caixa[14] if caixa[14] else "-"
    for linha in texto.split("\n"):
        c.drawString(50, y, linha)
        y -= 15

    # Assinatura
    y -= 50
    c.line(50, y, 300, y)
    c.drawString(50, y - 15, "Assinatura do Operador")

    c.save()
    print(f"Relatório gerado: {nome_arquivo}")

    # 🧠 Abre o PDF automaticamente após gerar (apenas Windows)
    try:
        os.startfile(nome_arquivo)
    except Exception as e:
        print(f"Erro ao abrir PDF automaticamente: {e}")