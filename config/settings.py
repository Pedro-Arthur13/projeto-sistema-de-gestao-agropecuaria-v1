DB_PATH = "fazenda_sertao.db"
SYSTEM_NAME = "Sistema de Gestao Agropecuaria - Fazenda Sertao"
SYSTEM_VERSION = "2.0"

DATA_INICIO_SISTEMA = (2026, 5, 11)

TIPOS_USUARIO = ("SUPERUSUARIO", "ADM", "CLIENTE")
TIPOS_ANIMAL = ("Bovino de Leite", "Caprino", "Ovino", "Suino/Leitao")

STATUS_ANIMAL_VENDA = "Disponivel para venda"
STATUS_ANIMAL_VENDIDO = "Vendido"
STATUS_ANIMAL_LACTACAO = "Lactacao"

SUPERUSUARIO_PADRAO = {
    "nome": "Super Admin",
    "email": "super@fazendasertao.com.br",
    "senha": "super123",
    "tipo": "SUPERUSUARIO",
    "prefixo": "",
}

PERMISSOES = {
    "SUPERUSUARIO": {
        "ver_tudo", "estoque_global", "historico_global", "compras_global",
        "agendamentos_global", "restaurar_registros", "exclusao_permanente",
        "gerenciar_adms", "promover_usuarios", "exportar_relatorios_globais",
        "dashboard_global", "ver_usuarios",
    },
    "ADM": {
        "gerenciar_rebanho", "gerenciar_producao", "ver_estoque_proprio",
        "ver_historico_proprio", "dashboard_proprio", "exportar_proprio",
        "ver_compras_proprias",
    },
    "CLIENTE": {
        "ver_estoque", "efetuar_compra", "ver_historico_compras", "agendar_retirada",
    },
}

RECIBOS_DIR = "recibos"
GRAFICOS_DIR = "graficos"
EXPORTS_DIR = "exportacoes"
