from reportlab.pdfgen import canvas
import os
from datetime import datetime

def gerar_dav_pdf(venda_id, itens, total, desconto, forma_pagamento, cliente_nome="Consumidor Final"):
    pasta = "notas_emitidas/dav"
    os.makedirs(pasta, exist_ok=True)

    caminho_pdf = os.path.join(pasta, f"DAV_{venda_id}.pdf")
    c = canvas.Canvas(caminho_pdf)
    y = 800

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y, "DOCUMENTO AUXILIAR DE VENDA (DAV)")
    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(100, y, f"Venda nº: {venda_id}")
    y -= 20
    c.drawString(100, y, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    y -= 20
    c.drawString(100, y, f"Cliente: {cliente_nome}")
    y -= 30

    c.setFont("Helvetica-Bold", 10)
    c.drawString(100, y, "Itens:")
    y -= 20
    c.setFont("Helvetica", 10)

    for item in itens:
        nome = item['nome']
        qtd = item['quantidade']
        preco = item['preco_unitario']
        subtotal = item['subtotal']
        linha = f"{nome[:30]} - {qtd} x R$ {preco:.2f} = R$ {subtotal:.2f}"
        c.drawString(100, y, linha)
        y -= 15
        if y < 100:
            c.showPage()
            y = 800

    y -= 10
    c.setFont("Helvetica-Bold", 10)
    c.drawString(100, y, f"DESCONTO: R$ {desconto:.2f}")
    y -= 15
    c.drawString(100, y, f"TOTAL: R$ {total:.2f}")
    y -= 15
    c.drawString(100, y, f"Pagamento: {forma_pagamento}")
    y -= 30
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(100, y, "Este documento não possui valor fiscal. Válido apenas como comprovante de venda.")
    c.save()

    # Abrir o PDF gerado automaticamente (opcional)
    try:
        os.startfile(caminho_pdf)
    except:
        pass
