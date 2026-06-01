import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from persistence.memoria import inicializar_sistema
from app.utils import separador, pausar
from config.settings import SYSTEM_NAME, SYSTEM_VERSION
from app import auth, fazenda, compras as compras_mod, dashboard as dash

sessao = {"usuario": None}


def usuario_logado():
    return sessao["usuario"]


def fazer_login():
    separador("LOGIN")
    email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()
    usuario = auth.login(email, senha)
    if usuario:
        sessao["usuario"] = usuario
        print(f"\nBem-vindo, {usuario['nome']} ({usuario['tipo']})!")
    else:
        print("E-mail ou senha invalidos.")


def fazer_logout():
    sessao["usuario"] = None
    print("Logout realizado.")


def cadastrar_usuario_menu():
    separador("CADASTRAR USUARIO")
    nome = input("Nome: ").strip()
    email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()
    tipo = input("Tipo (ADM/CLIENTE): ").strip().upper()
    ok, msg = auth.cadastrar_usuario(nome, email, senha, tipo, solicitante=usuario_logado())
    print(msg)


def menu_rebanho(adm):
    while True:
        separador("GERENCIAR REBANHO")
        print("1. Cadastrar Animal")
        print("2. Buscar Animal")
        print("3. Atualizar Status")
        print("4. Remover Animal")
        print("5. Listar Animais (meus)")
        print("0. Voltar")
        op = input("Opcao: ").strip()

        if op == "1":
            tipo = input("Tipo (Bovino de Leite/Caprino/Ovino/Suino/Leitao): ").strip()
            aid = input("ID (brinco/numero): ").strip()
            peso = input("Peso (kg): ").strip()
            preco = input("Preco de venda (R$): ").strip()
            status = input("Status: ").strip()
            ok, msg = fazenda.cadastrar_animal(tipo, aid, peso, preco, status, adm)
            print(msg)

        elif op == "2":
            aid = input("ID do animal (sem prefixo): ").strip()
            animal = fazenda.buscar_animal(aid, adm)
            if animal:
                print(f"  ID: {animal['id']} | Tipo: {animal['tipo']} | Peso: {animal['peso']} kg | Status: {animal['status']} | Preco: R$ {animal['preco_venda']:.2f}")
            else:
                print("Animal nao encontrado.")

        elif op == "3":
            aid = input("ID do animal (sem prefixo): ").strip()
            novo_status = input("Novo status: ").strip()
            ok, msg = fazenda.atualizar_status_animal(aid, novo_status, adm)
            print(msg)

        elif op == "4":
            aid = input("ID do animal (sem prefixo): ").strip()
            ok, msg = fazenda.remover_animal(aid, adm)
            print(msg)

        elif op == "5":
            animais = fazenda.listar_animais_adm(adm)
            if not animais:
                print("Nenhum animal cadastrado.")
            else:
                separador("Seus Animais", char="-")
                for a in animais:
                    print(f"  {a['id']:<12} {a['tipo']:<20} {a['peso']} kg  {a['status']:<30}  R$ {a['preco_venda']:.2f}")

        elif op == "0":
            break
        else:
            print("Opcao invalida.")
        pausar()


def menu_producao(adm):
    while True:
        separador("GERENCIAR PRODUCAO")
        print("1. Adicionar Leite")
        print("2. Adicionar Produto Derivado")
        print("3. Listar Estoque")
        print("0. Voltar")
        op = input("Opcao: ").strip()

        if op == "1":
            litros = input("Litros de leite: ").strip()
            preco = input("Preco por litro (R$): ").strip()
            ok, msg = fazenda.adicionar_leite(litros, preco, adm)
            print(msg)

        elif op == "2":
            nome = input("Nome do produto: ").strip()
            unidades = input("Quantidade de unidades: ").strip()
            peso_unit = input("Peso por unidade (kg): ").strip()
            preco = input("Preco de venda (R$/kg): ").strip()
            derivado_str = input("E derivado de leite? (s/n): ").strip().lower()
            derivado = derivado_str == "s"
            litros_unit = ""
            if derivado:
                litros_unit = input("Litros de leite por unidade: ").strip()
            ok, msg = fazenda.adicionar_produto(nome, unidades, peso_unit, preco, derivado, litros_unit, adm)
            print(msg)

        elif op == "3":
            estoque = fazenda.obter_estoque_leite_adm(adm)
            if estoque:
                print(f"\n  Leite: {estoque['litros']:.2f} L  a  R$ {estoque['preco_litro']:.2f}/L")
            else:
                print("\n  Leite: 0 L")
            produtos = fazenda.listar_produtos_adm(adm)
            print("\n  Produtos:")
            if not produtos:
                print("  Nenhum produto.")
            for p in produtos:
                tag = "(derivado)" if p["derivado"] else ""
                print(f"    {p['nome']:<25} {p['peso_total']:.2f} kg   R$ {p['preco_kg']:.2f}/kg {tag}")

        elif op == "0":
            break
        else:
            print("Opcao invalida.")
        pausar()


def menu_historico_adm(adm):
    separador("HISTORICO DE MOVIMENTACAO")
    registros = dash.historico_movimentacao(filtro_usuario=adm["email"])
    if not registros:
        print("Nenhuma movimentacao registrada.")
    else:
        for r in registros:
            print(f"  [{r['data']}] {r['acao']:<35} {r['item']}")


def menu_dashboard_adm(adm):
    while True:
        separador("DASHBOARD ADM")
        print("1. Ver Dashboard")
        print("2. Exportar (PNG)")
        print("3. Exportar (CSV)")
        print("4. Exportar (PDF)")
        print("5. Exportar Tudo")
        print("0. Voltar")
        op = input("Opcao: ").strip()
        if op == "1":
            dash.dashboard_adm(adm)
        elif op == "2":
            dash.exportar_dashboard_adm(adm, "png")
        elif op == "3":
            dash.exportar_dashboard_adm(adm, "csv")
        elif op == "4":
            dash.exportar_dashboard_adm(adm, "pdf")
        elif op == "5":
            dash.exportar_dashboard_adm(adm, "todos")
        elif op == "0":
            break
        else:
            print("Opcao invalida.")
        pausar()


def menu_adm(adm):
    while True:
        separador(f"MENU ADM — {adm['nome']}")
        print("1. Gerenciar Rebanho")
        print("2. Gerenciar Producao e Derivados")
        print("3. Dashboard e Relatorios")
        print("4. Historico de Movimentacao")
        print("5. Logout")
        op = input("Opcao: ").strip()

        if op == "1":
            menu_rebanho(adm)
        elif op == "2":
            menu_producao(adm)
        elif op == "3":
            menu_dashboard_adm(adm)
        elif op == "4":
            menu_historico_adm(adm)
            pausar()
        elif op == "5":
            fazer_logout()
            break
        else:
            print("Opcao invalida.")


def menu_estoque_cliente():
    separador("ESTOQUE DISPONIVEL")
    estoques = fazenda.listar_todo_estoque_leite()
    print("\nLeite:")
    if not estoques:
        print("  Nenhum leite disponivel.")
    for e in estoques:
        print(f"  ADM: {e['adm_email']} | {e['litros']:.2f} L | R$ {e['preco_litro']:.2f}/L")

    print("\nProdutos:")
    produtos = [p for p in fazenda.listar_todos_produtos() if p["peso_total"] > 0]
    if not produtos:
        print("  Nenhum produto disponivel.")
    for p in produtos:
        print(f"  {p['nome']:<25} ADM: {p['adm_email']} | {p['peso_total']:.2f} kg | R$ {p['preco_kg']:.2f}/kg")

    print("\nAnimais:")
    animais = fazenda.listar_animais_disponiveis()
    if not animais:
        print("  Nenhum animal disponivel para venda.")
    for a in animais:
        print(f"  {a['id']:<12} {a['tipo']:<20} ADM: {a['adm_email']} | R$ {a['preco_venda']:.2f}")


def menu_compra_cliente(cliente):
    separador("EFETUAR COMPRA")
    print("1. Comprar Produto")
    print("2. Comprar Animal")
    print("3. Comprar Leite")
    print("0. Voltar")
    op = input("Opcao: ").strip()

    if op == "1":
        produtos = [p for p in fazenda.listar_todos_produtos() if p["peso_total"] > 0]
        if not produtos:
            print("Nenhum produto disponivel.")
            return
        print("Produtos disponiveis:")
        for p in produtos:
            print(f"  {p['nome']:<25} | {p['peso_total']:.2f} kg | R$ {p['preco_kg']:.2f}/kg")
        nome = input("Nome do produto: ").strip()
        qty = input("Quantidade (kg): ").strip()
        ok, msg = compras_mod.comprar_produto(cliente, nome, qty)
        print(msg)

    elif op == "2":
        animais = fazenda.listar_animais_disponiveis()
        if not animais:
            print("Nenhum animal disponivel.")
            return
        for a in animais:
            print(f"  {a['id']:<12} {a['tipo']:<20} R$ {a['preco_venda']:.2f}")
        aid = input("ID do animal: ").strip()
        ok, msg = compras_mod.comprar_animal(cliente, aid)
        print(msg)

    elif op == "3":
        estoques = fazenda.listar_todo_estoque_leite()
        total = sum(e["litros"] for e in estoques)
        if total <= 0:
            print("Nenhum leite disponivel.")
            return
        qty = input("Quantidade (L): ").strip()
        ok, msg = compras_mod.comprar_leite(cliente, qty)
        print(msg)


def menu_historico_cliente(cliente):
    separador("HISTORICO DE COMPRAS")
    compras = compras_mod.historico_compras_cliente(cliente["email"])
    if not compras:
        print("Nenhuma compra registrada.")
    else:
        for c in compras:
            total = c["quantidade"] * c["preco_unitario"]
            print(f"  #{c['id']} | {c['tipo']:<8} | {c['item']:<25} | Qtd: {c['quantidade']}  | R$ {total:.2f} | Vendedor: {c['vendedor']}")
    separador("RETIRADAS AGENDADAS", char="-")
    agendamentos = compras_mod.historico_agendamentos_cliente(cliente["email"])
    if not agendamentos:
        print("Nenhum agendamento.")
    else:
        for ag in agendamentos:
            print(f"  {ag['tipo']:<10} {ag['item']:<25} {ag['data']} {ag['hora']}  CEP: {ag['cep']}")
            if ag["alerta_clima"]:
                print(f"    AVISO: {ag['alerta_clima']}")


def menu_cliente(cliente):
    while True:
        separador(f"MENU CLIENTE — {cliente['nome']}")
        print("1. Visualizar Estoque")
        print("2. Efetuar Compra")
        print("3. Historico de Compras e Retiradas")
        print("4. Logout")
        op = input("Opcao: ").strip()

        if op == "1":
            menu_estoque_cliente()
            pausar()
        elif op == "2":
            menu_compra_cliente(cliente)
            pausar()
        elif op == "3":
            menu_historico_cliente(cliente)
            pausar()
        elif op == "4":
            fazer_logout()
            break
        else:
            print("Opcao invalida.")


def menu_gerenciar_usuarios_super(su):
    while True:
        separador("GERENCIAR USUARIOS")
        print("1. Listar todos os usuarios")
        print("2. Promover/Rebaixar usuario")
        print("3. Desativar usuario")
        print("4. Restaurar usuario")
        print("5. Excluir permanentemente")
        print("0. Voltar")
        op = input("Opcao: ").strip()

        if op == "1":
            usuarios = auth.listar_usuarios()
            for u in usuarios:
                print(f"  [{u['tipo']:<12}] {u['nome']:<20} {u['email']}")
        elif op == "2":
            email = input("E-mail do usuario: ").strip()
            novo_tipo = input("Novo tipo (ADM/CLIENTE/SUPERUSUARIO): ").strip().upper()
            ok, msg = auth.promover_usuario(email, novo_tipo, su)
            print(msg)
        elif op == "3":
            email = input("E-mail do usuario: ").strip()
            ok, msg = auth.desativar_usuario(email, su)
            print(msg)
        elif op == "4":
            email = input("E-mail do usuario: ").strip()
            ok, msg = auth.restaurar_usuario(email, su)
            print(msg)
        elif op == "5":
            email = input("E-mail do usuario: ").strip()
            confirma = input(f"Tem certeza que deseja excluir {email} PERMANENTEMENTE? (sim): ").strip().lower()
            if confirma == "sim":
                ok, msg = auth.deletar_usuario_permanente(email, su)
                print(msg)
            else:
                print("Cancelado.")
        elif op == "0":
            break
        else:
            print("Opcao invalida.")
        pausar()


def menu_historico_global():
    separador("HISTORICO GLOBAL")
    registros = dash.historico_movimentacao(limite=50)
    for r in registros:
        print(f"  [{r['data']}] {r['acao']:<35} {r['item']:<25} | {r['usuario']}")


def menu_dashboard_super(su):
    while True:
        separador("DASHBOARD SUPERUSUARIO")
        print("1. Ver Dashboard Global")
        print("2. Exportar PNG")
        print("3. Exportar CSV")
        print("4. Exportar PDF")
        print("5. Exportar Tudo")
        print("0. Voltar")
        op = input("Opcao: ").strip()
        if op == "1":
            dash.dashboard_superusuario()
        elif op == "2":
            dash.exportar_dashboard_global(su, "png")
        elif op == "3":
            dash.exportar_dashboard_global(su, "csv")
        elif op == "4":
            dash.exportar_dashboard_global(su, "pdf")
        elif op == "5":
            dash.exportar_dashboard_global(su, "todos")
        elif op == "0":
            break
        else:
            print("Opcao invalida.")
        pausar()


def menu_superusuario(su):
    while True:
        separador(f"MENU SUPERUSUARIO — {su['nome']}")
        print("1. Gerenciar Usuarios")
        print("2. Dashboard Global")
        print("3. Historico Global")
        print("4. Gerenciar Rebanho (global)")
        print("5. Logout")
        op = input("Opcao: ").strip()

        if op == "1":
            menu_gerenciar_usuarios_super(su)
        elif op == "2":
            menu_dashboard_super(su)
        elif op == "3":
            menu_historico_global()
            pausar()
        elif op == "4":
            separador("REBANHO GLOBAL")
            todos = fazenda.listar_todos_animais()
            for a in todos:
                print(f"  {a['id']:<12} {a['tipo']:<20} {a['status']:<30} ADM: {a['adm_email']}")
            pausar()
        elif op == "5":
            fazer_logout()
            break
        else:
            print("Opcao invalida.")


def menu_principal_deslogado():
    separador(f"{SYSTEM_NAME} v{SYSTEM_VERSION}")
    print("1. Login")
    print("2. Cadastrar Usuario")
    print("3. Sair")
    op = input("Opcao: ").strip()
    if op == "1":
        fazer_login()
    elif op == "2":
        cadastrar_usuario_menu()
    elif op == "3":
        print("Ate logo!")
        sys.exit(0)
    else:
        print("Opcao invalida.")


def main():
    inicializar_sistema()
    while True:
        u = usuario_logado()
        if u is None:
            menu_principal_deslogado()
        elif u["tipo"] == "SUPERUSUARIO":
            menu_superusuario(u)
        elif u["tipo"] == "ADM":
            menu_adm(u)
        else:
            menu_cliente(u)


if __name__ == "__main__":
    main()
