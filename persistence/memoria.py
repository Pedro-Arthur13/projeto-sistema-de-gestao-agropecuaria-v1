from persistence import database as db

USUARIOS = []
ANIMAIS = []
ESTOQUE_LEITE = []
PRODUTOS = []
COMPRAS = []
AGENDAMENTOS = []
ENDERECOS = []
HISTORICO_MOVIMENTACAO = []
RELATORIOS_EXPORTADOS = []

LISTAS = {
    "usuarios": USUARIOS,
    "animais": ANIMAIS,
    "estoque_leite": ESTOQUE_LEITE,
    "produtos": PRODUTOS,
    "compras": COMPRAS,
    "agendamentos": AGENDAMENTOS,
    "enderecos": ENDERECOS,
    "historico_movimentacao": HISTORICO_MOVIMENTACAO,
    "relatorios_exportados": RELATORIOS_EXPORTADOS,
}

TABELAS_SEM_ATIVO = frozenset({"historico_movimentacao", "relatorios_exportados"})

EMAILS_USUARIOS = set()
IDS_ANIMAIS = set()


def _combina(registro, condicoes, valores):
    if not condicoes:
        return True
    for campo, valor in zip(condicoes, valores):
        if registro.get(campo) != valor:
            return False
    return True


def _ordenar(resultado, ordem):
    if ordem == "id DESC":
        resultado.sort(key=lambda r: r.get("id", 0), reverse=True)
    elif ordem == "id ASC":
        resultado.sort(key=lambda r: r.get("id", 0))


def _reconstruir_indices():
    EMAILS_USUARIOS.clear()
    IDS_ANIMAIS.clear()
    for u in USUARIOS:
        EMAILS_USUARIOS.add(u["email"])
    for a in ANIMAIS:
        IDS_ANIMAIS.add(a["id"])


def carregar_do_banco():
    for tabela, lista in LISTAS.items():
        lista.clear()
        lista.extend(db.buscar_todos(tabela))
    _reconstruir_indices()


def inicializar_sistema():
    db.inicializar_banco()
    carregar_do_banco()


def buscar_um(tabela, condicoes, valores):
    for registro in LISTAS[tabela]:
        if _combina(registro, condicoes, valores):
            return registro
    return None


def buscar_todos(tabela, condicoes=None, valores=None, ordem=None):
    resultado = []
    for registro in LISTAS[tabela]:
        if _combina(registro, condicoes, valores):
            resultado.append(registro)
    if ordem:
        _ordenar(resultado, ordem)
    return resultado


def inserir(tabela, dados):
    registro = dict(dados)
    if "ativo" not in registro and tabela not in TABELAS_SEM_ATIVO:
        registro["ativo"] = 1
    novo_id = db.inserir(tabela, registro)
    if novo_id and "id" not in registro:
        registro["id"] = novo_id
    LISTAS[tabela].append(registro)
    if tabela == "usuarios":
        EMAILS_USUARIOS.add(registro["email"])
    elif tabela == "animais":
        IDS_ANIMAIS.add(registro["id"])
    return registro.get("id", novo_id)


def atualizar(tabela, dados, condicoes, valores_condicoes):
    registro = buscar_um(tabela, condicoes, valores_condicoes)
    if not registro:
        return
    registro.update(dados)
    db.atualizar(tabela, dados, condicoes, valores_condicoes)


def soft_delete(tabela, condicoes, valores):
    atualizar(tabela, {"ativo": 0}, condicoes, valores)


def restaurar(tabela, condicoes, valores):
    atualizar(tabela, {"ativo": 1}, condicoes, valores)


def deletar_permanente(tabela, condicoes, valores):
    registro = buscar_um(tabela, condicoes, valores)
    if not registro:
        return
    lista = LISTAS[tabela]
    lista[:] = [r for r in lista if r is not registro]
    if tabela == "usuarios":
        EMAILS_USUARIOS.discard(registro["email"])
    elif tabela == "animais":
        IDS_ANIMAIS.discard(registro["id"])
    db.deletar_permanente(tabela, condicoes, valores)
