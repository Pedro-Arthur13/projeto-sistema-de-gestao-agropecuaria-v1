from persistence.memoria import buscar_um, buscar_todos, inserir, atualizar, COMPRAS, AGENDAMENTOS
from app.utils import validar_float_positivo, validar_data_hora, validar_cep, timestamp_agora
from app.api import buscar_endereco_por_cep, buscar_previsao_tempo
from config.settings import STATUS_ANIMAL_VENDA, STATUS_ANIMAL_VENDIDO, RECIBOS_DIR
from app import pdf


def _registrar_historico(acao, item, quantidade, usuario_email):
    inserir("historico_movimentacao", {
        "data": timestamp_agora(),
        "acao": acao,
        "item": item,
        "quantidade": quantidade,
        "usuario": usuario_email,
    })


def _salvar_endereco(endereco, cliente_email):
    inserir("enderecos", {
        "cep": endereco.get("cep", ""),
        "logradouro": endereco.get("logradouro", ""),
        "bairro": endereco.get("bairro", ""),
        "cidade": endereco.get("cidade", ""),
        "uf": endereco.get("uf", ""),
        "cliente": cliente_email,
    })


def _coletar_agendamento(cliente_email):
    data = input("Data de retirada (DD/MM/AAAA): ").strip()
    hora = input("Horario de retirada (HH:MM): ").strip()
    if not validar_data_hora(data, hora):
        return None, None, None, "Data ou hora invalida ou retroativa."
    cep_input = input("CEP para entrega (8 digitos): ").strip()
    ok_cep, cep_limpo = validar_cep(cep_input)
    if not ok_cep:
        return None, None, None, "CEP invalido. Informe 8 digitos numericos."
    endereco = buscar_endereco_por_cep(cep_limpo)
    alerta = ""
    if endereco:
        print(f"  Endereco: {endereco['logradouro']}, {endereco['bairro']} — {endereco['cidade']}/{endereco['uf']}")
        _salvar_endereco(endereco, cliente_email)
        previsao = buscar_previsao_tempo(endereco["uf"], data, hora)
        if previsao and previsao["alerta"]:
            alerta = previsao["alerta"]
            print(f"\n  AVISO CLIMATICO: {alerta}\n")
            print("  Recomendamos considerar reagendamento, mas voce pode prosseguir.")
    else:
        print("  CEP nao encontrado na base ViaCEP. Prosseguindo com CEP informado.")
        endereco = {"cep": cep_limpo, "logradouro": "", "bairro": "", "cidade": "", "uf": ""}
    return data, hora, endereco, alerta


def comprar_produto(cliente, nome_produto, qty_str):
    if not validar_float_positivo(qty_str):
        return False, "Quantidade invalida."
    qty = float(qty_str)
    candidatos = [
        p for p in buscar_todos("produtos", ["nome", "ativo"], [nome_produto, 1])
        if p["peso_total"] >= qty
    ]
    if not candidatos:
        return False, "Nenhum vendedor com estoque suficiente para este produto."
    print("\nVendedores disponiveis:")
    for p in candidatos:
        print(f"  - {p['adm_email']} | R$ {p['preco_kg']:.2f}/kg")
    vendedor_email = input("De qual vendedor deseja comprar? (e-mail): ").strip()
    produto = next((p for p in candidatos if p["adm_email"] == vendedor_email), None)
    if not produto:
        return False, "Vendedor nao encontrado ou estoque insuficiente."

    data, hora, endereco, alerta = _coletar_agendamento(cliente["email"])
    if endereco is None:
        return False, alerta

    novo_peso = produto["peso_total"] - qty
    atualizar("produtos", {"peso_total": novo_peso}, ["id"], [produto["id"]])

    compra_id = inserir("compras", {
        "cliente": cliente["email"],
        "tipo": "produto",
        "item": nome_produto,
        "quantidade": qty,
        "preco_unitario": produto["preco_kg"],
        "vendedor": vendedor_email,
    })
    inserir("agendamentos", {
        "cliente": cliente["email"],
        "item": nome_produto,
        "tipo": "produto",
        "data": data,
        "hora": hora,
        "cep": endereco["cep"],
        "logradouro": endereco["logradouro"],
        "bairro": endereco["bairro"],
        "cidade": endereco["cidade"],
        "uf": endereco["uf"],
        "alerta_clima": alerta,
    })
    _registrar_historico("venda_produto", nome_produto, qty, cliente["email"])

    vendedor = buscar_um("usuarios", ["email"], [vendedor_email])
    pdf.gerar_recibo({
        "id_pedido": compra_id,
        "cliente": cliente,
        "vendedor": vendedor or {"nome": vendedor_email, "email": vendedor_email},
        "itens": [{"item": nome_produto, "tipo": "produto", "quantidade": qty, "preco_unitario": produto["preco_kg"]}],
        "data": data,
        "hora": hora,
        "endereco": endereco,
        "alerta_clima": alerta,
    })
    return True, f"Compra realizada! Recibo gerado em '{RECIBOS_DIR}/'."


def comprar_animal(cliente, animal_id):
    animal = buscar_um("animais", ["id", "status", "ativo"], [animal_id, STATUS_ANIMAL_VENDA, 1])
    if not animal:
        return False, "Animal nao disponivel para venda."

    data, hora, endereco, alerta = _coletar_agendamento(cliente["email"])
    if endereco is None:
        return False, alerta

    atualizar("animais", {"status": STATUS_ANIMAL_VENDIDO}, ["id"], [animal_id])
    compra_id = inserir("compras", {
        "cliente": cliente["email"],
        "tipo": "animal",
        "item": animal_id,
        "quantidade": 1,
        "preco_unitario": animal["preco_venda"],
        "vendedor": animal["adm_email"],
    })
    inserir("agendamentos", {
        "cliente": cliente["email"],
        "item": animal_id,
        "tipo": "animal",
        "data": data,
        "hora": hora,
        "cep": endereco["cep"],
        "logradouro": endereco["logradouro"],
        "bairro": endereco["bairro"],
        "cidade": endereco["cidade"],
        "uf": endereco["uf"],
        "alerta_clima": alerta,
    })
    _registrar_historico("venda_animal", animal_id, 1, cliente["email"])

    vendedor = buscar_um("usuarios", ["email"], [animal["adm_email"]])
    pdf.gerar_recibo({
        "id_pedido": compra_id,
        "cliente": cliente,
        "vendedor": vendedor or {"nome": animal["adm_email"], "email": animal["adm_email"]},
        "itens": [{"item": animal_id, "tipo": "animal", "quantidade": 1, "preco_unitario": animal["preco_venda"]}],
        "data": data,
        "hora": hora,
        "endereco": endereco,
        "alerta_clima": alerta,
    })
    return True, f"Animal comprado! Recibo gerado em '{RECIBOS_DIR}/'."


def comprar_leite(cliente, qty_str):
    if not validar_float_positivo(qty_str):
        return False, "Quantidade invalida."
    qty = float(qty_str)
    estoques = [e for e in buscar_todos("estoque_leite", ["ativo"], [1]) if e["litros"] >= qty]
    if not estoques:
        return False, "Nenhum vendedor com leite suficiente disponivel."
    print("\nVendedores de leite disponiveis:")
    for e in estoques:
        print(f"  - {e['adm_email']} | {e['litros']} L | R$ {e['preco_litro']:.2f}/L")
    vendedor_email = input("De qual vendedor deseja comprar? (e-mail): ").strip()
    estoque = next((e for e in estoques if e["adm_email"] == vendedor_email), None)
    if not estoque:
        return False, "Vendedor nao encontrado ou leite insuficiente."

    data, hora, endereco, alerta = _coletar_agendamento(cliente["email"])
    if endereco is None:
        return False, alerta

    novo_litros = estoque["litros"] - qty
    atualizar("estoque_leite", {"litros": novo_litros}, ["adm_email"], [vendedor_email])
    compra_id = inserir("compras", {
        "cliente": cliente["email"],
        "tipo": "leite",
        "item": "Leite",
        "quantidade": qty,
        "preco_unitario": estoque["preco_litro"],
        "vendedor": vendedor_email,
    })
    inserir("agendamentos", {
        "cliente": cliente["email"],
        "item": "Leite",
        "tipo": "retirada",
        "data": data,
        "hora": hora,
        "cep": endereco["cep"],
        "logradouro": endereco["logradouro"],
        "bairro": endereco["bairro"],
        "cidade": endereco["cidade"],
        "uf": endereco["uf"],
        "alerta_clima": alerta,
    })
    _registrar_historico("venda_leite", "Leite", qty, cliente["email"])

    vendedor = buscar_um("usuarios", ["email"], [vendedor_email])
    pdf.gerar_recibo({
        "id_pedido": compra_id,
        "cliente": cliente,
        "vendedor": vendedor or {"nome": vendedor_email, "email": vendedor_email},
        "itens": [{"item": "Leite", "tipo": "leite", "quantidade": qty, "preco_unitario": estoque["preco_litro"]}],
        "data": data,
        "hora": hora,
        "endereco": endereco,
        "alerta_clima": alerta,
    })
    return True, f"Compra de leite realizada! Recibo gerado em '{RECIBOS_DIR}/'."


def historico_compras_cliente(cliente_email):
    return buscar_todos("compras", ["cliente"], [cliente_email], ordem="id DESC")


def historico_agendamentos_cliente(cliente_email):
    return buscar_todos("agendamentos", ["cliente"], [cliente_email], ordem="id DESC")


def obter_lista_compras():
    return COMPRAS


def obter_lista_agendamentos():
    return AGENDAMENTOS
