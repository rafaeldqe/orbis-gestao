from xml.dom import minidom
from reportlab.pdfgen import canvas
import os
import smtplib
from email.message import EmailMessage
import mimetypes

def gerar_danfe_pdf(caminho_xml, pasta_destino="notas_emitidas/pdf", email_destinatario=None):
    os.makedirs(pasta_destino, exist_ok=True)

    # Lê e parseia o XML
    doc = minidom.parse(caminho_xml)

    # Extrai dados básicos
    venda_id = doc.getElementsByTagName("infNFe")[0].getAttribute("Id")[-8:]
    emitente = doc.getElementsByTagName("xNome")[0].firstChild.data
    forma_pgto = doc.getElementsByTagName("tPag")[0].firstChild.data
    total = doc.getElementsByTagName("vNF")[0].firstChild.data

    itens = doc.getElementsByTagName("det")

    nome_pdf = os.path.splitext(os.path.basename(caminho_xml))[0] + ".pdf"
    caminho_pdf = os.path.join(pasta_destino, nome_pdf)

    c = canvas.Canvas(caminho_pdf)
    y = 800

    # Cabeçalho
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y, "DANFE - Documento Auxiliar da Nota Fiscal Eletrônica")
    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(100, y, f"Número da NF-e: {venda_id}")
    y -= 20
    c.drawString(100, y, f"Emitente: {emitente}")
    y -= 20
    c.drawString(100, y, f"Forma de Pagamento: {forma_pgto}")
    y -= 30

    # Itens
    c.setFont("Helvetica-Bold", 10)
    c.drawString(100, y, "Itens da Nota:")
    y -= 20
    c.setFont("Helvetica", 10)

    for item in itens:
        nome = item.getElementsByTagName("xProd")[0].firstChild.data
        qtd = item.getElementsByTagName("qCom")[0].firstChild.data
        preco = item.getElementsByTagName("vUnCom")[0].firstChild.data
        subtotal = item.getElementsByTagName("vProd")[0].firstChild.data
        linha = f"{nome[:30]} - {qtd} x R$ {preco} = R$ {subtotal}"
        c.drawString(100, y, linha)
        y -= 15
        if y < 100:
            c.showPage()
            y = 800

    y -= 10
    c.setFont("Helvetica-Bold", 10)
    c.drawString(100, y, f"TOTAL: R$ {total}")
    y -= 30
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(100, y, "Este documento é uma representação simplificada da NF-e.")
    c.save()

    # Imprimir automaticamente
    try:
        os.startfile(caminho_pdf, "print")
    except:
        print("Impressão automática falhou ou não suportada.")

    # Enviar por e-mail (opcional)
    if email_destinatario:
        try:
            enviar_email_com_pdf(caminho_pdf, email_destinatario)
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")

    # Abrir o PDF
    try:
        os.startfile(caminho_pdf)
    except:
        pass

def enviar_email_com_pdf(arquivo_pdf, destinatario):
    remetente = "seu_email@gmail.com"  # Substituir pelo seu
    senha = "sua_senha_de_app"         # Senha de app do Gmail (ou similar)

    msg = EmailMessage()
    msg["Subject"] = "DANFE - Nota Fiscal da sua compra"
    msg["From"] = remetente
    msg["To"] = destinatario
    msg.set_content("Olá, segue em anexo a DANFE referente à sua compra.\n\nObrigado!")

    with open(arquivo_pdf, "rb") as f:
        tipo, _ = mimetypes.guess_type(arquivo_pdf)
        tipo = tipo or "application/pdf"
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=os.path.basename(arquivo_pdf))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remetente, senha)
        smtp.send_message(msg)
