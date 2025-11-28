import sqlite3
from pathlib import Path

DB_PATH = Path("database.db")

def get_connection():
    return sqlite3.connect(DB_PATH)


# ===========================================
# Inicialização do Banco de Dados
# ===========================================
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Tabela de materiais
    cur.execute("""
        CREATE TABLE IF NOT EXISTS materiais (
            id_material INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_material TEXT UNIQUE NOT NULL,
            unidade TEXT NOT NULL,
            quantidade_adquirida REAL NOT NULL,
            custo_total REAL NOT NULL
        )
    """)

    # Tabela de tecidos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tecidos (
            id_tecido INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_tecido TEXT UNIQUE NOT NULL,
            comprimento_total REAL NOT NULL,
            largura_total REAL NOT NULL,
            custo_total REAL NOT NULL
        )
    """)

    # Tabela de mão de obra (somente 1 registro)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS configuracoes (
            id INTEGER PRIMARY KEY,
            valor_hora REAL NOT NULL,
            margem_lucro REAL NOT NULL
        )
    """)

    # Tabela de peças
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pecas (
            id_peca INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_peca TEXT UNIQUE NOT NULL,
            tempo_producao_horas REAL NOT NULL,
            preco_sugerido REAL DEFAULT 0
        )
    """)

    # Tabela N-N: materiais usados em peças
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pecas_materiais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            peca_id INTEGER NOT NULL,
            material_id INTEGER NOT NULL,
            quantidade_usada REAL NOT NULL,
            FOREIGN KEY (peca_id) REFERENCES pecas(id_peca),
            FOREIGN KEY (material_id) REFERENCES materiais(id_material)
        )
    """)

    # Tabela N-N: tecidos usados em peças
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pecas_tecidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            peca_id INTEGER NOT NULL,
            tecido_id INTEGER NOT NULL,
            area_usada_cm2 REAL NOT NULL,
            FOREIGN KEY (peca_id) REFERENCES pecas(id_peca),
            FOREIGN KEY (tecido_id) REFERENCES tecidos(id_tecido)
        )
    """)

    # MIGRAÇÃO → adicionar preco_sugerido se não existir
    cur.execute("PRAGMA table_info(pecas)")
    colunas = [c[1] for c in cur.fetchall()]
    if "preco_sugerido" not in colunas:
        cur.execute("ALTER TABLE pecas ADD COLUMN preco_sugerido REAL DEFAULT 0")

    conn.commit()
    conn.close()


init_db()


# ===========================================
#  FUNÇÕES — MATERIAIS
# ===========================================
def nome_material_existe(nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM materiais WHERE nome_material=?", (nome,))
    row = cur.fetchone()
    conn.close()
    return row is not None


def listar_materiais():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_material, nome_material, unidade, quantidade_adquirida, custo_total
        FROM materiais
        ORDER BY nome_material ASC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def inserir_material(nome, unidade, qtd, custo):
    conn = get_connection()
    conn.execute("""
        INSERT INTO materiais (nome_material, unidade, quantidade_adquirida, custo_total)
        VALUES (?, ?, ?, ?)
    """, (nome, unidade, qtd, custo))
    conn.commit()
    conn.close()


def atualizar_material(id_material, nome, unidade, qtd, custo):
    conn = get_connection()
    conn.execute("""
        UPDATE materiais SET nome_material=?, unidade=?, quantidade_adquirida=?, custo_total=?
        WHERE id_material=?
    """, (nome, unidade, qtd, custo, id_material))
    conn.commit()
    conn.close()


def excluir_material(id_material):
    conn = get_connection()
    conn.execute("DELETE FROM materiais WHERE id_material=?", (id_material,))
    conn.commit()
    conn.close()


# ===========================================
#  FUNÇÕES — TECIDOS
# ===========================================
def nome_tecido_existe(nome):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM tecidos WHERE nome_tecido=?", (nome,))
    row = cur.fetchone()
    conn.close()
    return row is not None


def listar_tecidos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_tecido, nome_tecido, comprimento_total, largura_total, custo_total
        FROM tecidos
        ORDER BY nome_tecido ASC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def inserir_tecido(nome, comp, larg, custo):
    conn = get_connection()
    conn.execute("""
        INSERT INTO tecidos (nome_tecido, comprimento_total, largura_total, custo_total)
        VALUES (?, ?, ?, ?)
    """, (nome, comp, larg, custo))
    conn.commit()
    conn.close()


def atualizar_tecido(id_tecido, nome, comp, larg, custo):
    conn = get_connection()
    conn.execute("""
        UPDATE tecidos SET nome_tecido=?, comprimento_total=?, largura_total=?, custo_total=?
        WHERE id_tecido=?
    """, (nome, comp, larg, custo, id_tecido))
    conn.commit()
    conn.close()


def excluir_tecido(id_tecido):
    conn = get_connection()
    conn.execute("DELETE FROM tecidos WHERE id_tecido=?", (id_tecido,))
    conn.commit()
    conn.close()


# ===========================================
#  FUNÇÕES — MÃO DE OBRA
# ===========================================
def salvar_configuracoes(valor_hora, margem):
    conn = get_connection()
    conn.execute("DELETE FROM configuracoes")
    conn.execute("""
        INSERT INTO configuracoes (id, valor_hora, margem_lucro)
        VALUES (1, ?, ?)
    """, (valor_hora, margem))
    conn.commit()
    conn.close()


def carregar_configuracoes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT valor_hora, margem_lucro FROM configuracoes WHERE id=1")
    row = cur.fetchone()
    conn.close()
    if row:
        return {"valor_hora": row[0], "margem": row[1]}
    return {"valor_hora": 0, "margem": 0}


# ===========================================
#  FUNÇÕES — PEÇAS
# ===========================================
def listar_pecas():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_peca, nome_peca, tempo_producao_horas, preco_sugerido
        FROM pecas ORDER BY nome_peca ASC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_peca(peca_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_peca, nome_peca, tempo_producao_horas, preco_sugerido
        FROM pecas WHERE id_peca=?
    """, (peca_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "id_peca": row[0],
            "nome_peca": row[1],
            "tempo_producao_horas": row[2],
            "preco_sugerido": row[3]
        }
    return None


def inserir_peca(nome, tempo):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO pecas (nome_peca, tempo_producao_horas)
        VALUES (?, ?)
    """, (nome, tempo))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def atualizar_peca(peca_id, nome, tempo):
    conn = get_connection()
    conn.execute("""
        UPDATE pecas
        SET nome_peca=?, tempo_producao_horas=?
        WHERE id_peca=?
    """, (nome, tempo, peca_id))
    conn.commit()
    conn.close()


def excluir_peca(peca_id):
    conn = get_connection()
    cur = conn.cursor()

    # Apagar relações com materiais
    cur.execute("DELETE FROM pecas_materiais WHERE peca_id=?", (peca_id,))

    # Apagar relações com tecidos
    cur.execute("DELETE FROM pecas_tecidos WHERE peca_id=?", (peca_id,))

    # Apagar a peça
    cur.execute("DELETE FROM pecas WHERE id_peca=?", (peca_id,))

    conn.commit()
    conn.close()




def salvar_preco_sugerido(peca_id, preco):
    conn = get_connection()
    conn.execute("""
        UPDATE pecas SET preco_sugerido=? WHERE id_peca=?
    """, (preco, peca_id))
    conn.commit()
    conn.close()


# ===============================================
# Relações N-N entre peças, materiais e tecidos
# ===============================================
def materiais_da_peca(peca_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT pm.material_id, pm.quantidade_usada, m.nome_material
        FROM pecas_materiais pm
        JOIN materiais m ON pm.material_id = m.id_material
        WHERE pm.peca_id=?
    """, (peca_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def tecidos_da_peca(peca_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT pt.tecido_id, pt.area_usada_cm2, t.nome_tecido
        FROM pecas_tecidos pt
        JOIN tecidos t ON pt.tecido_id = t.id_tecido
        WHERE pt.peca_id=?
    """, (peca_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def limpar_relacoes_peca(peca_id):
    conn = get_connection()
    conn.execute("DELETE FROM pecas_materiais WHERE peca_id=?", (peca_id,))
    conn.execute("DELETE FROM pecas_tecidos WHERE peca_id=?", (peca_id,))
    conn.commit()
    conn.close()


def adicionar_material_na_peca(peca_id, material_id, qtd):
    conn = get_connection()
    conn.execute("""
        INSERT INTO pecas_materiais (peca_id, material_id, quantidade_usada)
        VALUES (?, ?, ?)
    """, (peca_id, material_id, qtd))
    conn.commit()
    conn.close()


def adicionar_tecido_na_peca(peca_id, tecido_id, area):
    conn = get_connection()
    conn.execute("""
        INSERT INTO pecas_tecidos (peca_id, tecido_id, area_usada_cm2)
        VALUES (?, ?, ?)
    """, (peca_id, tecido_id, area))
    conn.commit()
    conn.close()


# ===============================================
# Cálculo completo de custos e preço sugerido
# ===============================================
def compute_peca_cost(peca_id):
    peca = get_peca(peca_id)
    if not peca:
        return None

    cfg = carregar_configuracoes()
    valor_hora = cfg["valor_hora"]
    margem = cfg["margem"]

    materiais = materiais_da_peca(peca_id)
    tecidos = tecidos_da_peca(peca_id)

    custo_materiais = 0
    custo_tecidos = 0

    conn = get_connection()
    cur = conn.cursor()

    # custo proporcional dos materiais
    for mid, qtd, _ in materiais:
        cur.execute("SELECT custo_total, quantidade_adquirida FROM materiais WHERE id_material=?", (mid,))
        ctotal, qadq = cur.fetchone()
        custo_materiais += (ctotal / qadq) * qtd

    # custo proporcional dos tecidos
    for tid, area, _ in tecidos:
        cur.execute("SELECT custo_total, comprimento_total, largura_total FROM tecidos WHERE id_tecido=?", (tid,))
        ctotal, comp, larg = cur.fetchone()
        area_total = comp * larg
        custo_tecidos += (ctotal / area_total) * area

    # custo de mão de obra
    custo_mao = peca["tempo_producao_horas"] * valor_hora

    # soma total
    custo_total = custo_materiais + custo_tecidos + custo_mao

    # preço sugerido com margem de lucro
    preco_final = custo_total * (1 + margem / 100)

    return {
        "custo_materiais": custo_materiais,
        "custo_tecidos": custo_tecidos,
        "custo_mao_de_obra": custo_mao,
        "custo_total": custo_total,
        "preco_sugerido": preco_final,
    }
