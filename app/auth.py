from persistence.memoria import (
    buscar_um, buscar_todos, inserir, atualizar,
    soft_delete, restaurar, deletar_permanente,
    USUARIOS, EMAILS_USUARIOS,
)
from app.utils import validar_email, gerar_prefixo, timestamp_agora
from config.settings import PERMISSOES


def login(email, senha):
    return buscar_um("usuarios", ["email", "senha", "ativo"], [email, senha, 1])


def cadastrar_usuario(nome, email, senha, tipo, solicitante=None):
    if not validar_email(email):
        return False, "E-mail inválido (formato esperado: algo@algo.algo)."
    if email in EMAILS_USUARIOS or buscar_um("usuarios", ["email"], [email]):
        return False, "E-mail já cadastrado."
    if tipo not in ("ADM", "CLIENTE", "SUPERUSUARIO"):
        return False, "Tipo inválido."
    if tipo == "SUPERUSUARIO":
        if solicitante is None or solicitante.get("tipo") != "SUPERUSUARIO":
            return False, "Apenas SUPERUSUARIO pode criar outro SUPERUSUARIO."

    prefixo = ""
    if tipo == "ADM":
        todos = buscar_todos("usuarios")
        prefixo = gerar_prefixo(nome, todos)

    inserir("usuarios", {
        "nome": nome,
        "email": email,
        "senha": senha,
        "tipo": tipo,
        "prefixo": prefixo,
    })
    _registrar_historico("cadastro_usuario", f"{tipo}:{email}", 0, email)
    return True, "Usuário cadastrado com sucesso."


def listar_usuarios(tipo_filtro=None):
    if tipo_filtro:
        return buscar_todos("usuarios", ["tipo", "ativo"], [tipo_filtro, 1])
    return buscar_todos("usuarios", ["ativo"], [1])


def obter_lista_usuarios():
    return USUARIOS


def promover_usuario(email_alvo, novo_tipo, solicitante):
    if solicitante.get("tipo") != "SUPERUSUARIO":
        return False, "Apenas SUPERUSUARIO pode promover/rebaixar usuários."
    usuario = buscar_um("usuarios", ["email", "ativo"], [email_alvo, 1])
    if not usuario:
        return False, "Usuário não encontrado."
    if novo_tipo not in ("ADM", "CLIENTE", "SUPERUSUARIO"):
        return False, "Tipo inválido."
    prefixo = usuario.get("prefixo", "")
    if novo_tipo == "ADM" and usuario["tipo"] != "ADM":
        todos = buscar_todos("usuarios")
        prefixo = gerar_prefixo(usuario["nome"], todos)
    atualizar("usuarios", {"tipo": novo_tipo, "prefixo": prefixo}, ["email"], [email_alvo])
    _registrar_historico("promocao_usuario", email_alvo, 0, solicitante["email"])
    return True, f"Usuário {email_alvo} promovido para {novo_tipo}."


def desativar_usuario(email_alvo, solicitante):
    if solicitante.get("tipo") != "SUPERUSUARIO":
        return False, "Apenas SUPERUSUARIO pode desativar usuários."
    soft_delete("usuarios", ["email"], [email_alvo])
    _registrar_historico("desativacao_usuario", email_alvo, 0, solicitante["email"])
    return True, "Usuário desativado."


def restaurar_usuario(email_alvo, solicitante):
    if solicitante.get("tipo") != "SUPERUSUARIO":
        return False, "Apenas SUPERUSUARIO pode restaurar usuários."
    restaurar("usuarios", ["email"], [email_alvo])
    _registrar_historico("restauracao_usuario", email_alvo, 0, solicitante["email"])
    return True, "Usuário restaurado."


def deletar_usuario_permanente(email_alvo, solicitante):
    if solicitante.get("tipo") != "SUPERUSUARIO":
        return False, "Apenas SUPERUSUARIO pode excluir permanentemente."
    deletar_permanente("usuarios", ["email"], [email_alvo])
    _registrar_historico("exclusao_permanente_usuario", email_alvo, 0, solicitante["email"])
    return True, "Usuário excluído permanentemente."


def tem_permissao(usuario, permissao):
    tipo = usuario.get("tipo", "CLIENTE")
    return permissao in PERMISSOES.get(tipo, set())


def _registrar_historico(acao, item, quantidade, usuario_email):
    inserir("historico_movimentacao", {
        "data": timestamp_agora(),
        "acao": acao,
        "item": item,
        "quantidade": quantidade,
        "usuario": usuario_email,
    })
