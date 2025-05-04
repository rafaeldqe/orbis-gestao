import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from datetime import datetime
import control.vendas_controller as vendas_controller

def gerar_xml_nfe(venda_id, pasta_destino="notas_emitidas/xmls"):
    # Cria pasta se não existir
    os.makedirs(pasta_destino, exist_ok=True)

    # Dados da venda
    venda, itens = vendas_controller.detalhar_venda(venda_id)

    # XML raiz
    nfe = Element("NFe")

    # InfNFe
    infnfe = SubElement(nfe, "infNFe", Id="NFe12345678901234567890123456789012345678901234", versao="4.00")

    # Emitente (fixo por enquanto)
    emit = SubElement(infnfe, "emit")
    SubElement(emit, "CNPJ").text = "12345678000195"
    SubElement(emit, "xNome").text = "Orbis Gestão Ltda"
    SubElement(emit, "enderEmit")
    SubElement(emit, "IE").text = "1234567890"
    SubElement(emit, "CRT").text = "3"  # Simples Nacional

    # Destinatário
    dest = SubElement(infnfe, "dest")
    SubElement(dest, "CPF").text = "00000000191"  # Pode variar
    SubElement(dest, "xNome").text = "Consumidor Final"

    # Itens
    for i, item in enumerate(itens, start=1):
        det = SubElement(infnfe, "det", nItem=str(i))
        prod = SubElement(det, "prod")
        SubElement(prod, "cProd").text = str(i)
        SubElement(prod, "xProd").text = item[0]
        SubElement(prod, "qCom").text = str(item[1])
        SubElement(prod, "vUnCom").text = f"{item[2]:.2f}"
        SubElement(prod, "vProd").text = f"{item[3]:.2f}"
        SubElement(prod, "CFOP").text = "5102"
        SubElement(prod, "uCom").text = "UN"

        imposto = SubElement(det, "imposto")
        icms = SubElement(imposto, "ICMS")
        SubElement(icms, "CST").text = "102"

    # Totais
    total = SubElement(infnfe, "total")
    icmstot = SubElement(total, "ICMSTot")
    SubElement(icmstot, "vProd").text = f"{venda[1]:.2f}"
    SubElement(icmstot, "vNF").text = f"{venda[1]:.2f}"

    # Pagamento
    pag = SubElement(infnfe, "pag")
    detPag = SubElement(pag, "detPag")
    SubElement(detPag, "tPag").text = "01"  # 01 = Dinheiro
    SubElement(detPag, "vPag").text = f"{venda[1]:.2f}"

    # Gera XML formatado
    xml_bruto = tostring(nfe, encoding="utf-8")
    xml_formatado = minidom.parseString(xml_bruto).toprettyxml(indent="  ")

    # Salva o XML
    nome_arquivo = f"NFe_{venda_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xml"
    caminho = os.path.join(pasta_destino, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(xml_formatado)

    return caminho
