import sqlite3
from config.settings import DB_PATH, SUPERUSUARIO_PADRAO, STATUS_ANIMAL_VENDA


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def inicializar_banco():
    conn = conectar()
    cur = conn.cursor()

    cur.executescript(f"""
        CREATE TABLE IF NOT EXISTS usuarios (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nome        TEXT    NOT NULL,
            email       TEXT    NOT NULL UNIQUE,
            senha       TEXT    NOT NULL,
            tipo        TEXT    NOT NULL DEFAULT 'CLIENTE',
            prefixo     TEXT    DEFAULT '',
            ativo       INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS animais (
            id          TEXT    PRIMARY KEY,
            tipo        TEXT    NOT NULL,
            peso        REAL    NOT NULL DEFAULT 0,
            preco_venda REAL    NOT NULL DEFAULT 0,
            status      TEXT    NOT NULL DEFAULT '{STATUS_ANIMAL_VENDA}',
            adm_email   TEXT    NOT NULL,
            ativo       INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS estoque_leite (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            adm_email   TEXT    NOT NULL UNIQUE,
            litros      REAL    NOT NULL DEFAULT 0,
            preco_litro REAL    NOT NULL DEFAULT 0,
            ativo       INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS produtos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nome        TEXT    NOT NULL,
            peso_total  REAL    NOT NULL DEFAULT 0,
            preco_kg    REAL    NOT NULL DEFAULT 0,
            derivado    INTEGER NOT NULL DEFAULT 0,
            leite_usado REAL    NOT NULL DEFAULT 0,
            adm_email   TEXT    NOT NULL,
            ativo       INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS compras (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente         TEXT    NOT NULL,
            tipo            TEXT    NOT NULL,
            item            TEXT    NOT NULL,
            quantidade      REAL    NOT NULL,
            preco_unitario  REAL    NOT NULL DEFAULT 0,
            vendedor        TEXT    NOT NULL,
            ativo           INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS agendamentos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente     TEXT    NOT NULL,
            item        TEXT    NOT NULL,
            tipo        TEXT    NOT NULL,
            data        TEXT    NOT NULL,
            hora        TEXT    NOT NULL,
            cep         TEXT    DEFAULT '',
            logradouro  TEXT    DEFAULT '',
            bairro      TEXT    DEFAULT '',
            cidade      TEXT    DEFAULT '',
            uf          TEXT    DEFAULT '',
            alerta_clima TEXT   DEFAULT '',
            ativo       INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS enderecos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            cep         TEXT    NOT NULL,
            logradouro  TEXT    DEFAULT '',
            bairro      TEXT    DEFAULT '',
            cidade      TEXT    DEFAULT '',
            uf          TEXT    DEFAULT '',
            cliente     TEXT    DEFAULT '',
            ativo       INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS historico_movimentacao (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            data        TEXT    NOT NULL,
            acao        TEXT    NOT NULL,
            item        TEXT    NOT NULL,
            quantidade  REAL    DEFAULT 0,
            usuario     TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS relatorios_exportados (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            data        TEXT    NOT NULL,
            tipo        TEXT    NOT NULL,
            formato     TEXT    NOT NULL,
            caminho     TEXT    NOT NULL,
            usuario     TEXT    NOT NULL
        );
    """)

    conn.commit()
    _criar_superusuario_padrao(conn)
    conn.close()


def _criar_superusuario_padrao(conn):
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM usuarios WHERE email = ?",
        (SUPERUSUARIO_PADRAO["email"],),
    )
    if cur.fetchone():
        return
    cur.execute(
        """INSERT INTO usuarios (nome, email, senha, tipo, prefixo)
           VALUES (?, ?, ?, ?, ?)""",
        (
            SUPERUSUARIO_PADRAO["nome"],
            SUPERUSUARIO_PADRAO["email"],
            SUPERUSUARIO_PADRAO["senha"],
            SUPERUSUARIO_PADRAO["tipo"],
            SUPERUSUARIO_PADRAO["prefixo"],
        ),
    )
    conn.commit()


def buscar_um(tabela, condicoes, valores):
    conn = conectar()
    cur = conn.cursor()
    where = " AND ".join(f"{c} = ?" for c in condicoes)
    cur.execute(f"SELECT * FROM {tabela} WHERE {where}", valores)
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def buscar_todos(tabela, condicoes=None, valores=None, ordem=None):
    conn = conectar()
    cur = conn.cursor()
    sql = f"SELECT * FROM {tabela}"
    if condicoes:
        where = " AND ".join(f"{c} = ?" for c in condicoes)
        sql += f" WHERE {where}"
    if ordem:
        sql += f" ORDER BY {ordem}"
    cur.execute(sql, valores or [])
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def inserir(tabela, dados):
    conn = conectar()
    cur = conn.cursor()
    colunas = ", ".join(dados.keys())
    placeholders = ", ".join("?" for _ in dados)
    cur.execute(
        f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})",
        list(dados.values()),
    )
    novo_id = cur.lastrowid
    conn.commit()
    conn.close()
    return novo_id


def atualizar(tabela, dados, condicoes, valores_condicoes):
    conn = conectar()
    cur = conn.cursor()
    set_clause = ", ".join(f"{c} = ?" for c in dados.keys())
    where = " AND ".join(f"{c} = ?" for c in condicoes)
    cur.execute(
        f"UPDATE {tabela} SET {set_clause} WHERE {where}",
        list(dados.values()) + list(valores_condicoes),
    )
    conn.commit()
    conn.close()


def soft_delete(tabela, condicoes, valores):
    atualizar(tabela, {"ativo": 0}, condicoes, valores)


def restaurar(tabela, condicoes, valores):
    atualizar(tabela, {"ativo": 1}, condicoes, valores)


def deletar_permanente(tabela, condicoes, valores):
    conn = conectar()
    cur = conn.cursor()
    where = " AND ".join(f"{c} = ?" for c in condicoes)
    cur.execute(f"DELETE FROM {tabela} WHERE {where}", valores)
    conn.commit()
    conn.close()


def executar_sql(sql, valores=None):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(sql, valores or [])
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return [dict(r) for r in rows]
