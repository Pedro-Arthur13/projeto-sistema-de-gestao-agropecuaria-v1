import os
import csv
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from persistence.database import buscar_todos, buscar_um, inserir
from app.utils import separador, timestamp_agora
from config.settings import GRAFICOS_DIR, EXPORTS_DIR, SYSTEM_NAME


def _garantir_diretorios():
    os.makedirs(GRAFICOS_DIR, exist_ok=True)
    os.makedirs(EXPORTS_DIR, exist_ok=True)


def _registrar_exportacao(tipo, formato, caminho, usuario_email):
    inserir("relatorios_exportados", {
        "data": timestamp_agora(),
        "tipo": tipo,
        "formato": formato,
        "caminho": caminho,
        "usuario": usuario_email,
    })


def _gerar_grafico_animais_por_tipo(animais, prefixo_arquivo):
    _garantir_diretorios()
    contagem = {}
    for a in animais:
        contagem[a["tipo"]] = contagem.get(a["tipo"], 0) + 1
    if not contagem:
        print("  Sem dados de animais para grafico.")
        return None

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=list(contagem.keys()), y=list(contagem.values()), palette="viridis", ax=ax)
    ax.set_title("Distribuicao de Animais por Tipo")
    ax.set_xlabel("Tipo")
    ax.set_ylabel("Quantidade")
    plt.tight_layout()
    caminho = os.path.join(GRAFICOS_DIR, f"{prefixo_arquivo}_animais.png")
    fig.savefig(caminho, dpi=120)
    plt.close(fig)
    return caminho


def _gerar_grafico_vendas(compras, prefixo_arquivo):
    _garantir_diretorios()
    contagem = {}
    for c in compras:
        contagem[c["tipo"]] = contagem.get(c["tipo"], 0) + (c["quantidade"] * c["preco_unitario"])
    if not contagem:
        print("  Sem dados de vendas para grafico.")
        return None

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=list(contagem.keys()), y=list(contagem.values()), palette="rocket", ax=ax)
    ax.set_title("Receita por Categoria")
    ax.set_xlabel("Categoria")
    ax.set_ylabel("Receita (R$)")
    plt.tight_layout()
    caminho = os.path.join(GRAFICOS_DIR, f"{prefixo_arquivo}_vendas.png")
    fig.savefig(caminho, dpi=120)
    plt.close(fig)
    return caminho


def _gerar_grafico_estoque_leite(estoques, prefixo_arquivo):
    _garantir_diretorios()
    if not estoques:
        print("  Sem dados de leite para grafico.")
        return None
    emails = [e["adm_email"].split("@")[0] for e in estoques]
    litros = [e["litros"] for e in estoques]

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=emails, y=litros, palette="mako", ax=ax)
    ax.set_title("Estoque de Leite por ADM")
    ax.set_xlabel("ADM")
    ax.set_ylabel("Litros")
    plt.tight_layout()
    caminho = os.path.join(GRAFICOS_DIR, f"{prefixo_arquivo}_leite.png")
    fig.savefig(caminho, dpi=120)
    plt.close(fig)
    return caminho


def _gerar_grafico_movimentacoes(historico, prefixo_arquivo):
    _garantir_diretorios()
    if not historico:
        return None
    contagem = {}
    for h in historico:
        contagem[h["acao"]] = contagem.get(h["acao"], 0) + 1

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=list(contagem.keys()), y=list(contagem.values()), palette="flare", ax=ax)
    ax.set_title("Movimentacoes por Acao")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    caminho = os.path.join(GRAFICOS_DIR, f"{prefixo_arquivo}_movimentacoes.png")
    fig.savefig(caminho, dpi=120)
    plt.close(fig)
    return caminho


def dashboard_adm(adm):
    separador("DASHBOARD ADM")
    animais = buscar_todos("animais", ["adm_email", "ativo"], [adm["email"], 1])
    por_tipo = {}
    for a in animais:
        por_tipo[a["tipo"]] = por_tipo.get(a["tipo"], 0) + 1

    print("\nAnimais por tipo:")
    for tipo, qtd in por_tipo.items():
        print(f"  {tipo:<25} {qtd:>5}")

    estoque_leite = buscar_um("estoque_leite", ["adm_email"], [adm["email"]])
    litros = estoque_leite["litros"] if estoque_leite else 0
    print(f"\n  Estoque de leite:     {litros:.2f} L")

    produtos = buscar_todos("produtos", ["adm_email", "ativo"], [adm["email"], 1])
    print("\nProdutos derivados:")
    for p in produtos:
        tag = "(derivado)" if p["derivado"] else ""
        print(f"  {p['nome']:<25} {p['peso_total']:.2f} kg   R$ {p['preco_kg']:.2f}/kg {tag}")

    compras = buscar_todos("compras", ["vendedor"], [adm["email"]])
    receita = sum(c["quantidade"] * c["preco_unitario"] for c in compras)
    print(f"\n  Receita total (vendas): R$ {receita:.2f}")
    print(f"  Total de vendas:        {len(compras)}")

    historico = buscar_todos("historico_movimentacao", ["usuario"], [adm["email"]], ordem="id DESC")
    print("\nUltimas movimentacoes:")
    for h in historico[:8]:
        print(f"  [{h['data']}] {h['acao']:<30} {h['item']}")

    separador()


def dashboard_superusuario():
    separador("DASHBOARD SUPERUSUARIO — GLOBAL")

    usuarios = buscar_todos("usuarios", ["ativo"], [1])
    adms = [u for u in usuarios if u["tipo"] == "ADM"]
    clientes = [u for u in usuarios if u["tipo"] == "CLIENTE"]
    print(f"\n  Usuarios ativos: {len(usuarios)}  (ADMs: {len(adms)}, Clientes: {len(clientes)})")

    animais = buscar_todos("animais", ["ativo"], [1])
    por_tipo = {}
    for a in animais:
        por_tipo[a["tipo"]] = por_tipo.get(a["tipo"], 0) + 1
    print("\nRebanho global:")
    for tipo, qtd in por_tipo.items():
        print(f"  {tipo:<25} {qtd:>5}")

    estoques = buscar_todos("estoque_leite", ["ativo"], [1])
    total_leite = sum(e["litros"] for e in estoques)
    print(f"\n  Leite total no sistema: {total_leite:.2f} L")

    compras = buscar_todos("compras")
    receita = sum(c["quantidade"] * c["preco_unitario"] for c in compras)
    print(f"\n  Receita global: R$ {receita:.2f}")
    print(f"  Total de compras: {len(compras)}")

    historico = buscar_todos("historico_movimentacao", ordem="id DESC")
    print("\nUltimas movimentacoes globais:")
    for h in historico[:10]:
        print(f"  [{h['data']}] {h['acao']:<30} {h['item']} | {h['usuario']}")

    separador()


def exportar_dashboard_adm(adm, formato):
    _garantir_diretorios()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefixo = f"adm_{adm['prefixo']}_{ts}"

    animais = buscar_todos("animais", ["adm_email", "ativo"], [adm["email"], 1])
    compras = buscar_todos("compras", ["vendedor"], [adm["email"]])
    estoque_leite = buscar_um("estoque_leite", ["adm_email"], [adm["email"]])
    estoques = [estoque_leite] if estoque_leite else []
    produtos = buscar_todos("produtos", ["adm_email", "ativo"], [adm["email"], 1])
    historico = buscar_todos("historico_movimentacao", ["usuario"], [adm["email"]], ordem="id DESC")

    arquivos = []

    if formato in ("png", "todos"):
        for g in [
            _gerar_grafico_animais_por_tipo(animais, prefixo),
            _gerar_grafico_vendas(compras, prefixo),
            _gerar_grafico_estoque_leite(estoques, prefixo),
            _gerar_grafico_movimentacoes(historico[:30], prefixo),
        ]:
            if g:
                arquivos.append(g)
                _registrar_exportacao("dashboard_adm", "png", g, adm["email"])

    if formato in ("csv", "todos"):
        caminho_csv = os.path.join(EXPORTS_DIR, f"{prefixo}_compras.csv")
        with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "cliente", "tipo", "item", "quantidade", "preco_unitario", "vendedor"])
            writer.writeheader()
            writer.writerows(compras)
        arquivos.append(caminho_csv)
        _registrar_exportacao("dashboard_adm", "csv", caminho_csv, adm["email"])

        caminho_csv2 = os.path.join(EXPORTS_DIR, f"{prefixo}_animais.csv")
        with open(caminho_csv2, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "tipo", "peso", "preco_venda", "status", "adm_email"])
            writer.writeheader()
            writer.writerows(animais)
        arquivos.append(caminho_csv2)
        _registrar_exportacao("dashboard_adm", "csv", caminho_csv2, adm["email"])

    if formato in ("pdf", "todos"):
        caminho_pdf = os.path.join(EXPORTS_DIR, f"{prefixo}_relatorio.pdf")
        _exportar_pdf_adm(adm, animais, compras, estoques, produtos, caminho_pdf)
        arquivos.append(caminho_pdf)
        _registrar_exportacao("dashboard_adm", "pdf", caminho_pdf, adm["email"])

    print(f"\n  Arquivos exportados ({len(arquivos)}):")
    for a in arquivos:
        print(f"    {a}")


def _exportar_pdf_adm(adm, animais, compras, estoques, produtos, caminho):
    from fpdf import FPDF
    p = FPDF()
    p.add_page()
    p.set_font("Helvetica", "B", 14)
    p.cell(0, 10, f"{SYSTEM_NAME} — Relatorio ADM", ln=True, align="C")
    p.set_font("Helvetica", "", 10)
    p.cell(0, 6, f"ADM: {adm['nome']} ({adm['email']})", ln=True)
    p.cell(0, 6, f"Gerado em: {timestamp_agora()}", ln=True)
    p.ln(4)

    p.set_font("Helvetica", "B", 11)
    p.cell(0, 8, "Animais", ln=True)
    p.set_font("Helvetica", "", 10)
    for a in animais:
        p.cell(0, 6, f"  {a['id']} | {a['tipo']} | {a['peso']} kg | {a['status']}", ln=True)

    p.ln(3)
    p.set_font("Helvetica", "B", 11)
    p.cell(0, 8, "Estoque de Leite", ln=True)
    p.set_font("Helvetica", "", 10)
    for e in estoques:
        p.cell(0, 6, f"  {e['litros']:.2f} L a R$ {e['preco_litro']:.2f}/L", ln=True)

    p.ln(3)
    p.set_font("Helvetica", "B", 11)
    p.cell(0, 8, "Produtos", ln=True)
    p.set_font("Helvetica", "", 10)
    for pr in produtos:
        p.cell(0, 6, f"  {pr['nome']} | {pr['peso_total']:.2f} kg | R$ {pr['preco_kg']:.2f}/kg", ln=True)

    p.ln(3)
    p.set_font("Helvetica", "B", 11)
    p.cell(0, 8, "Vendas", ln=True)
    p.set_font("Helvetica", "", 10)
    receita = sum(c["quantidade"] * c["preco_unitario"] for c in compras)
    p.cell(0, 6, f"  Total de vendas: {len(compras)}  |  Receita: R$ {receita:.2f}", ln=True)

    p.output(caminho)


def exportar_dashboard_global(superusuario, formato):
    _garantir_diretorios()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefixo = f"global_{ts}"

    animais = buscar_todos("animais", ["ativo"], [1])
    compras = buscar_todos("compras")
    estoques = buscar_todos("estoque_leite", ["ativo"], [1])
    historico = buscar_todos("historico_movimentacao", ordem="id DESC")

    arquivos = []

    if formato in ("png", "todos"):
        for g in [
            _gerar_grafico_animais_por_tipo(animais, prefixo),
            _gerar_grafico_vendas(compras, prefixo),
            _gerar_grafico_estoque_leite(estoques, prefixo),
            _gerar_grafico_movimentacoes(historico[:50], prefixo),
        ]:
            if g:
                arquivos.append(g)
                _registrar_exportacao("dashboard_global", "png", g, superusuario["email"])

    if formato in ("csv", "todos"):
        for nome, dados in [("compras", compras), ("animais", animais)]:
            if dados:
                caminho_csv = os.path.join(EXPORTS_DIR, f"{prefixo}_{nome}.csv")
                with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=list(dados[0].keys()))
                    writer.writeheader()
                    writer.writerows(dados)
                arquivos.append(caminho_csv)
                _registrar_exportacao("dashboard_global", "csv", caminho_csv, superusuario["email"])

    if formato in ("pdf", "todos"):
        caminho_pdf = os.path.join(EXPORTS_DIR, f"{prefixo}_relatorio.pdf")
        _exportar_pdf_adm(superusuario, animais, compras, estoques, [], caminho_pdf)
        arquivos.append(caminho_pdf)
        _registrar_exportacao("dashboard_global", "pdf", caminho_pdf, superusuario["email"])

    print(f"\n  Arquivos exportados ({len(arquivos)}):")
    for a in arquivos:
        print(f"    {a}")


def historico_movimentacao(filtro_usuario=None, limite=30):
    if filtro_usuario:
        registros = buscar_todos("historico_movimentacao", ["usuario"], [filtro_usuario], ordem="id DESC")
    else:
        registros = buscar_todos("historico_movimentacao", ordem="id DESC")
    return registros[:limite]
