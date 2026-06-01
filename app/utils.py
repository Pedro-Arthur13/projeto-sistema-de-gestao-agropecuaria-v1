import unicodedata
from datetime import datetime
from config.settings import DATA_INICIO_SISTEMA


def texto_pdf(texto):
    if texto is None:
        return ""
    s = str(texto)
    s = s.replace("\u2014", " - ").replace("\u2013", "-").replace("\u2022", "*")
    s = unicodedata.normalize("NFKD", s)
    return s.encode("ascii", "ignore").decode("ascii")


def timestamp_agora():
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def separador(titulo="", char="="):
    largura = 55
    if titulo:
        lado = (largura - len(titulo) - 2) // 2
        print(char * lado + " " + titulo + " " + char * lado)
    else:
        print(char * largura)


def pausar():
    input("\n[Enter para continuar...]")


def validar_email(email):
    at_count = 0
    at_idx = -1
    dot_idx = -1
    for i, c in enumerate(email):
        if c == "@":
            at_count += 1
            at_idx = i
        elif c == "." and at_count == 1:
            dot_idx = i
    return (
        at_count == 1
        and at_idx > 0
        and dot_idx > at_idx + 1
        and dot_idx < len(email) - 1
    )


def validar_float_positivo(valor_str):
    if not valor_str or valor_str == ".":
        return False
    dot_c = 0
    for c in valor_str:
        if c == ".":
            dot_c += 1
            if dot_c > 1:
                return False
        elif not c.isdigit():
            return False
    try:
        return float(valor_str) > 0
    except ValueError:
        return False


def validar_inteiro_positivo(valor_str):
    if not valor_str:
        return False
    for c in valor_str:
        if not c.isdigit():
            return False
    try:
        return int(valor_str) > 0
    except ValueError:
        return False


def validar_cep(cep):
    cep_limpo = cep.replace("-", "").replace(".", "").replace(" ", "").strip()
    if len(cep_limpo) != 8 or not cep_limpo.isdigit():
        return False, ""
    return True, cep_limpo


def _data_para_datetime(dd, mm, yy, hh, mn):
    try:
        return datetime(yy, mm, dd, hh, mn)
    except ValueError:
        return None


def validar_data_hora(data_str, hora_str):
    partes_data = data_str.split("/")
    partes_hora = hora_str.split(":")
    if len(partes_data) != 3 or len(partes_hora) != 2:
        return False
    for p in partes_data + partes_hora:
        if not p or not p.isdigit():
            return False
    dd, mm, yy = int(partes_data[0]), int(partes_data[1]), int(partes_data[2])
    hh, mn = int(partes_hora[0]), int(partes_hora[1])
    ano_min, mes_min, dia_min = DATA_INICIO_SISTEMA
    if (yy, mm, dd) < (ano_min, mes_min, dia_min):
        return False
    if not (1 <= mm <= 12 and 1 <= dd <= 31):
        return False
    if mm in (4, 6, 9, 11) and dd > 30:
        return False
    if mm == 2:
        bissexto = yy % 4 == 0 and (yy % 100 != 0 or yy % 400 == 0)
        if dd > 29 or (dd == 29 and not bissexto):
            return False
    if not (0 <= hh <= 23 and 0 <= mn <= 59):
        return False
    agendamento = _data_para_datetime(dd, mm, yy, hh, mn)
    if agendamento is None:
        return False
    if agendamento < datetime.now():
        return False
    return True


def normalizar_tipo_animal(raw):
    raw = (
        raw.strip()
        .lower()
        .replace("u\u00fa", "u")
        .replace("\u00fa", "u")
        .replace("\u00ed", "i")
        .replace("\u00e3", "a")
        .replace("\u00e7", "c")
        .replace("\u00f3", "o")
        .replace("\u00e9", "e")
    )
    mapa = {
        "bovino de leite": "Bovino de Leite",
        "caprino": "Caprino",
        "ovino": "Ovino",
        "suino/leitao": "Suino/Leitao",
        "suino leitao": "Suino/Leitao",
        "suino": "Suino/Leitao",
        "leitao": "Suino/Leitao",
        "suino/leit\u00e3o": "Suino/Leitao",
    }
    return mapa.get(raw)


def normalizar_status_animal(raw):
    from config.settings import STATUS_ANIMAL_VENDA
    raw_lower = (
        raw.strip()
        .lower()
        .replace("\u00fa", "u")
        .replace("\u00ed", "i")
        .replace("\u00e3", "a")
        .replace("\u00e7", "c")
        .replace("\u00f3", "o")
        .replace("\u00e9", "e")
    )
    if raw_lower in ("disponivel para venda", "disponivel"):
        return STATUS_ANIMAL_VENDA
    return raw.strip()


def gerar_prefixo(nome, usuarios_existentes):
    prefixo = nome[0].lower() if nome else "adm"
    i = 1
    while True:
        ja_usado = any(
            u["tipo"] == "ADM" and u["prefixo"] == prefixo
            for u in usuarios_existentes
        )
        if not ja_usado:
            break
        if i < len(nome):
            c = nome[i].lower()
            if c != " ":
                prefixo += c
            i += 1
        else:
            prefixo += "1"
    return prefixo
