import os
from datetime import datetime
from fpdf import FPDF
from config.settings import RECIBOS_DIR, SYSTEM_NAME
from app.utils import texto_pdf


def _garantir_diretorio(caminho):
    os.makedirs(caminho, exist_ok=True)


def _c(doc, largura, altura, conteudo, **kwargs):
    doc.cell(largura, altura, texto_pdf(conteudo), **kwargs)


def gerar_recibo(pedido):
    _garantir_diretorio(RECIBOS_DIR)
    pid = pedido.get("id_pedido", "0")
    cliente = pedido["cliente"]
    vendedor = pedido["vendedor"]
    itens = pedido["itens"]
    data_ret = pedido["data"]
    hora_ret = pedido["hora"]
    endereco = pedido.get("endereco", {})
    alerta = pedido.get("alerta_clima", "")

    total = sum(i["quantidade"] * i["preco_unitario"] for i in itens)

    doc = FPDF()
    doc.add_page()
    doc.set_auto_page_break(auto=True, margin=15)

    doc.set_font("Helvetica", "B", 16)
    _c(doc, 0, 10, SYSTEM_NAME, ln=True, align="C")
    doc.set_font("Helvetica", "", 10)
    _c(doc, 0, 6, f"Recibo de Compra - Pedido #{pid}", ln=True, align="C")
    _c(doc, 0, 6, f"Emitido em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
    doc.ln(4)

    doc.set_draw_color(100, 100, 100)
    doc.line(10, doc.get_y(), 200, doc.get_y())
    doc.ln(4)

    doc.set_font("Helvetica", "B", 11)
    _c(doc, 0, 8, "Dados do Cliente", ln=True)
    doc.set_font("Helvetica", "", 10)
    _c(doc, 0, 6, f"Nome: {cliente.get('nome', '')}", ln=True)
    _c(doc, 0, 6, f"E-mail: {cliente.get('email', '')}", ln=True)
    doc.ln(3)

    doc.set_font("Helvetica", "B", 11)
    _c(doc, 0, 8, "Dados do Vendedor", ln=True)
    doc.set_font("Helvetica", "", 10)
    _c(doc, 0, 6, f"Nome: {vendedor.get('nome', '')}", ln=True)
    _c(doc, 0, 6, f"E-mail: {vendedor.get('email', '')}", ln=True)
    doc.ln(3)

    doc.set_font("Helvetica", "B", 11)
    _c(doc, 0, 8, "Itens", ln=True)
    doc.set_font("Helvetica", "B", 10)
    _c(doc, 70, 7, "Item", border=1)
    _c(doc, 25, 7, "Tipo", border=1, align="C")
    _c(doc, 30, 7, "Qtd/Peso", border=1, align="C")
    _c(doc, 35, 7, "Preco Unit.", border=1, align="C")
    _c(doc, 30, 7, "Subtotal", border=1, align="C")
    doc.ln()
    doc.set_font("Helvetica", "", 10)
    for item in itens:
        subtotal = item["quantidade"] * item["preco_unitario"]
        unidade = "L" if item["tipo"] == "leite" else "kg" if item["tipo"] == "produto" else "un"
        _c(doc, 70, 7, str(item["item"]), border=1)
        _c(doc, 25, 7, item["tipo"].capitalize(), border=1, align="C")
        _c(doc, 30, 7, f"{item['quantidade']} {unidade}", border=1, align="C")
        _c(doc, 35, 7, f"R$ {item['preco_unitario']:.2f}", border=1, align="C")
        _c(doc, 30, 7, f"R$ {subtotal:.2f}", border=1, align="C")
        doc.ln()
    doc.set_font("Helvetica", "B", 11)
    _c(doc, 160, 8, "TOTAL", align="R")
    _c(doc, 30, 8, f"R$ {total:.2f}", border=1, align="C")
    doc.ln(6)

    doc.set_font("Helvetica", "B", 11)
    _c(doc, 0, 8, "Retirada Agendada", ln=True)
    doc.set_font("Helvetica", "", 10)
    _c(doc, 0, 6, f"Data: {data_ret}   Hora: {hora_ret}", ln=True)
    if endereco.get("logradouro") or endereco.get("cidade"):
        _c(doc, 0, 6, f"Endereco: {endereco.get('logradouro', '')}, {endereco.get('bairro', '')}", ln=True)
        _c(doc, 0, 6, f"Cidade: {endereco.get('cidade', '')}/{endereco.get('uf', '')}   CEP: {endereco.get('cep', '')}", ln=True)
    else:
        _c(doc, 0, 6, f"CEP: {endereco.get('cep', 'Nao informado')}", ln=True)

    if alerta:
        doc.ln(3)
        doc.set_fill_color(255, 220, 100)
        doc.set_font("Helvetica", "B", 10)
        _c(doc, 0, 8, f"  AVISO CLIMATICO: {alerta}", ln=True, fill=True)

    doc.ln(4)
    doc.line(10, doc.get_y(), 200, doc.get_y())
    doc.ln(3)
    doc.set_font("Helvetica", "I", 8)
    _c(doc, 0, 6, "Fazenda Sertao - Documento gerado automaticamente.", ln=True, align="C")

    nome_arquivo = os.path.join(RECIBOS_DIR, f"recibo_pedido_{pid}.pdf")
    doc.output(nome_arquivo)
    print(f"  PDF gerado: {nome_arquivo}")
    return nome_arquivo
