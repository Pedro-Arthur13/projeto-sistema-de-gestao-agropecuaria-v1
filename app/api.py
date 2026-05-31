import requests


def buscar_endereco_por_cep(cep):
    cep_limpo = cep.replace("-", "").replace(".", "").replace(" ", "").strip()
    if len(cep_limpo) != 8 or not cep_limpo.isdigit():
        return None
    try:
        resp = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=5)
        if resp.status_code != 200:
            return None
        dados = resp.json()
        if dados.get("erro"):
            return None
        return {
            "cep": dados.get("cep", cep_limpo),
            "logradouro": dados.get("logradouro", ""),
            "bairro": dados.get("bairro", ""),
            "cidade": dados.get("localidade", ""),
            "uf": dados.get("uf", ""),
        }
    except (requests.RequestException, ValueError):
        return None


_COORDS_POR_UF = {
    "AC": (-9.97, -67.81), "AL": (-9.66, -35.74), "AM": (-3.07, -60.02),
    "AP": (0.03, -51.07),  "BA": (-12.97, -38.51), "CE": (-3.71, -38.54),
    "DF": (-15.77, -47.93),"ES": (-20.32, -40.34), "GO": (-16.68, -49.25),
    "MA": (-2.53, -44.30), "MG": (-19.92, -43.94), "MS": (-20.44, -54.65),
    "MT": (-15.60, -56.10),"PA": (-1.46, -48.50),  "PB": (-7.12, -34.86),
    "PE": (-8.05, -34.88), "PI": (-5.09, -42.82),  "PR": (-25.43, -49.27),
    "RJ": (-22.91, -43.17),"RN": (-5.79, -35.21),  "RO": (-8.76, -63.90),
    "RR": (2.82, -60.67),  "RS": (-30.03, -51.23), "SC": (-27.59, -48.55),
    "SE": (-10.91, -37.07),"SP": (-23.55, -46.63), "TO": (-10.25, -48.32),
}


def buscar_previsao_tempo(uf, data_str, hora_str):
    coords = _COORDS_POR_UF.get(uf.upper())
    if not coords:
        return None
    lat, lon = coords
    try:
        partes = data_str.split("/")
        if len(partes) != 3:
            return None
        data_iso = f"{partes[2]}-{partes[1]}-{partes[0]}"
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&hourly=precipitation_probability,weathercode"
            f"&start_date={data_iso}&end_date={data_iso}"
            "&timezone=America%2FSao_Paulo"
        )
        resp = requests.get(url, timeout=8)
        if resp.status_code != 200:
            return None
        dados = resp.json()
        horas = dados.get("hourly", {}).get("time", [])
        prec_prob = dados.get("hourly", {}).get("precipitation_probability", [])
        wcodes = dados.get("hourly", {}).get("weathercode", [])
        target = f"{data_iso}T{hora_str}:00"
        prob, wcode = 0, 0
        if target in horas:
            idx = horas.index(target)
            prob = prec_prob[idx] if idx < len(prec_prob) else 0
            wcode = wcodes[idx] if idx < len(wcodes) else 0
        else:
            hora_int = int(hora_str.split(":")[0]) if ":" in hora_str else 12
            for i, h in enumerate(horas):
                if h.startswith(data_iso) and int(h[11:13]) == hora_int:
                    prob = prec_prob[i] if i < len(prec_prob) else 0
                    wcode = wcodes[i] if i < len(wcodes) else 0
                    break
        return {"prob_chuva": prob, "wcode": wcode, "alerta": _gerar_alerta(prob, wcode)}
    except (requests.RequestException, ValueError, KeyError):
        return None


def _gerar_alerta(prob_chuva, wcode):
    if wcode >= 95 or prob_chuva >= 80:
        return "TEMPESTADE/CHUVA INTENSA — Recomendado reagendar a retirada."
    if prob_chuva >= 50:
        return "CHUVA PROVAVEL — Considere reagendar a retirada."
    if prob_chuva >= 20:
        return "POSSIBILIDADE DE CHUVA — Esteja preparado."
    return ""
