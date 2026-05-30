from persistence.database import buscar_um, buscar_todos, inserir, atualizar, soft_delete
from app.utils import (
    validar_float_positivo,
    validar_inteiro_positivo,
    normalizar_tipo_animal,
    normalizar_status_animal,
    timestamp_agora,
)
from config.settings import STATUS_ANIMAL_VENDA, STATUS_ANIMAL_VENDIDO


def _registrar_historico(acao, item, quantidade, usuario_email):
    inserir("historico_movimentacao", {
        "data": timestamp_agora(),
        "acao": acao,
        "item": item,
        "quantidade": quantidade,
        "usuario": usuario_email,
    })


def cadastrar_animal(tipo_raw, id_bruto, peso_str, preco_str, status_raw, adm):
    tipo = normalizar_tipo_animal(tipo_raw)
    if not tipo:
        return False, "Tipo de animal inválido."
    animal_id = adm["prefixo"] + id_bruto
    if buscar_um("animais", ["id"], [animal_id]):
        return False, "Já existe um animal com este ID."
    if not validar_float_positivo(peso_str):
        return False, "Peso inválido."
    if not validar_float_positivo(preco_str):
        return False, "Preço inválido."
    status = normalizar_status_animal(status_raw)
    inserir("animais", {
        "id": animal_id,
        "tipo": tipo,
        "peso": float(peso_str),
        "preco_venda": float(preco_str),
        "status": status,
        "adm_email": adm["email"],
    })
    _registrar_historico("cadastro_animal", animal_id, float(peso_str), adm["email"])
    return True, f"Animal {animal_id} cadastrado."


def buscar_animal(id_bruto, adm):
    animal_id = adm["prefixo"] + id_bruto
    return buscar_um("animais", ["id", "ativo"], [animal_id, 1])


def atualizar_status_animal(id_bruto, novo_status_raw, adm):
    animal_id = adm["prefixo"] + id_bruto
    animal = buscar_um("animais", ["id", "ativo"], [animal_id, 1])
    if not animal:
        return False, "Animal não encontrado."
    status = normalizar_status_animal(novo_status_raw)
    atualizar("animais", {"status": status}, ["id"], [animal_id])
    _registrar_historico("alteracao_status_animal", animal_id, 0, adm["email"])
    return True, "Status atualizado."


def remover_animal(id_bruto, adm):
    animal_id = adm["prefixo"] + id_bruto
    animal = buscar_um("animais", ["id", "adm_email", "ativo"], [animal_id, adm["email"], 1])
    if not animal:
        return False, "Animal não encontrado."
    soft_delete("animais", ["id"], [animal_id])
    _registrar_historico("remocao_animal", animal_id, 0, adm["email"])
    return True, "Animal removido."


def listar_animais_adm(adm):
    return buscar_todos("animais", ["adm_email", "ativo"], [adm["email"], 1])


def listar_animais_disponiveis():
    return buscar_todos("animais", ["status", "ativo"], [STATUS_ANIMAL_VENDA, 1])


def listar_todos_animais():
    return buscar_todos("animais", ["ativo"], [1])


def adicionar_leite(litros_str, preco_str, adm):
    if not validar_float_positivo(litros_str):
        return False, "Litros inválidos."
    if not validar_float_positivo(preco_str):
        return False, "Preço inválido."
    litros = float(litros_str)
    preco = float(preco_str)
    estoque = buscar_um("estoque_leite", ["adm_email"], [adm["email"]])
    if estoque:
        novo_total = estoque["litros"] + litros
        atualizar("estoque_leite", {"litros": novo_total, "preco_litro": preco}, ["adm_email"], [adm["email"]])
    else:
        inserir("estoque_leite", {"adm_email": adm["email"], "litros": litros, "preco_litro": preco})
    _registrar_historico("adicao_leite", "Leite", litros, adm["email"])
    return True, f"{litros} L de leite adicionados ao estoque."


def adicionar_produto(nome, unidades_str, peso_unit_str, preco_str, derivado, litros_unit_str, adm):
    if not validar_inteiro_positivo(unidades_str):
        return False, "Quantidade de unidades inválida."
    if not validar_float_positivo(peso_unit_str):
        return False, "Peso por unidade inválido."
    if not validar_float_positivo(preco_str):
        return False, "Preço inválido."

    unidades = int(unidades_str)
    peso_unit = float(peso_unit_str)
    preco = float(preco_str)
    peso_total = unidades * peso_unit
    leite_usado = 0.0

    if derivado:
        if not validar_float_positivo(litros_unit_str):
            return False, "Litros de leite por unidade inválido."
        litros_unit = float(litros_unit_str)
        leite_usado = unidades * litros_unit
        estoque = buscar_um("estoque_leite", ["adm_email"], [adm["email"]])
        if not estoque or estoque["litros"] < leite_usado:
            return False, f"Leite insuficiente. Necessário: {leite_usado} L."
        novo_litros = estoque["litros"] - leite_usado
        atualizar("estoque_leite", {"litros": novo_litros}, ["adm_email"], [adm["email"]])
        _registrar_historico("consumo_leite_producao", nome, leite_usado, adm["email"])

    produtos = buscar_todos("produtos", ["adm_email", "nome", "ativo"], [adm["email"], nome, 1])
    if produtos:
        produto_existente = produtos[0]
        novo_peso = produto_existente["peso_total"] + peso_total
        atualizar("produtos", {"peso_total": novo_peso, "preco_kg": preco}, ["id"], [produto_existente["id"]])
    else:
        inserir("produtos", {
            "nome": nome,
            "peso_total": peso_total,
            "preco_kg": preco,
            "derivado": int(derivado),
            "leite_usado": leite_usado,
            "adm_email": adm["email"],
        })
    _registrar_historico("adicao_produto", nome, peso_total, adm["email"])
    return True, f"{peso_total} kg de {nome} adicionados ao estoque."


def listar_produtos_adm(adm):
    return buscar_todos("produtos", ["adm_email", "ativo"], [adm["email"], 1])


def listar_todos_produtos():
    return buscar_todos("produtos", ["ativo"], [1])


def obter_estoque_leite_adm(adm):
    return buscar_um("estoque_leite", ["adm_email"], [adm["email"]])


def listar_todo_estoque_leite():
    return buscar_todos("estoque_leite", ["ativo"], [1])
