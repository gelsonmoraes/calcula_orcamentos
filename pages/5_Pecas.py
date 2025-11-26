import streamlit as st
import database as db

st.title("🧩 Peças")

# Carregar listas
materiais = db.listar_materiais()
tecidos = db.listar_tecidos()
pecas = db.listar_pecas()

st.subheader("📋 Peças Cadastradas")

if pecas:
    for p in pecas:
        st.markdown(f"**{p[1]}** — Tempo: {p[2]}h — Preço Sugerido: R$ {p[3]:.2f}")
else:
    st.info("Nenhuma peça cadastrada ainda.")


st.divider()
st.subheader("➕ Cadastrar / ✏️ Editar Peça")

# Selecionar peça para edição
peca_escolhida = st.selectbox(
    "Selecione uma peça para editar ou escolha 'Nova peça'",
    ["Nova peça"] + [p[1] for p in pecas]
)

# ------------------------------------------
# Carregar dados da peça selecionada
# ------------------------------------------
edit_mode = False
peca_data = None

if peca_escolhida != "Nova peça":
    edit_mode = True
    peca_data = next(p for p in pecas if p[1] == peca_escolhida)
    peca_id = peca_data[0]

    dados_peca = db.get_peca(peca_id)
    mats_usados = db.materiais_da_peca(peca_id)
    tec_usados = db.tecidos_da_peca(peca_id)

else:
    peca_id = None
    dados_peca = None
    mats_usados = []
    tec_usados = []


# ------------------------------------------
# Formulário de cadastro / edição
# ------------------------------------------
st.write("### Dados da Peça")

nome = st.text_input(
    "Nome da Peça",
    value=dados_peca["nome_peca"] if edit_mode else ""
)

tempo = st.number_input(
    "Tempo de Produção (horas)",
    min_value=0.1, step=0.1,
    value=dados_peca["tempo_producao_horas"] if edit_mode else 1.0
)


st.write("### Materiais usados")
materiais_map = {m[1]: m for m in materiais}
sel_mats = st.multiselect(
    "Selecione os materiais",
    list(materiais_map.keys()),
    default=[m[2] for m in mats_usados] if edit_mode else []
)

quant_mats = {}
for nome_mat in sel_mats:
    mat = materiais_map[nome_mat]
    quant = st.number_input(f"Qtd usada de {nome_mat} ({mat[2]})", min_value=0.01, step=0.01)
    quant_mats[mat[0]] = quant


st.write("### Tecidos usados")
tecidos_map = {t[1]: t for t in tecidos}
sel_tecs = st.multiselect(
    "Selecione os tecidos",
    list(tecidos_map.keys()),
    default=[t[2] for t in tec_usados] if edit_mode else []
)

area_tecs = {}
for nome_tec in sel_tecs:
    t = tecidos_map[nome_tec]
    area = st.number_input(
        f"Área usada do tecido {nome_tec} (cm²)",
        min_value=1.0, step=1.0
    )
    area_tecs[t[0]] = area


# ------------------------------------------
# Botões de ação
# ------------------------------------------
col1, col2, col3 = st.columns(3)

if col1.button("💾 Salvar Peça"):
    if not edit_mode:
        # Criar nova peça
        novo_id = db.inserir_peca(nome, tempo)
        db.limpar_relacoes_peca(novo_id)

        # Salvar materiais
        for mid, qtd in quant_mats.items():
            db.adicionar_material_na_peca(novo_id, mid, qtd)

        # Salvar tecidos
        for tid, area in area_tecs.items():
            db.adicionar_tecido_na_peca(novo_id, tid, area)

        st.success("Peça cadastrada com sucesso! Atualize a página.")
    else:
        # Atualizar peça existente
        db.atualizar_peca(peca_id, nome, tempo)
        db.limpar_relacoes_peca(peca_id)

        # Regravar materiais
        for mid, qtd in quant_mats.items():
            db.adicionar_material_na_peca(peca_id, mid, qtd)

        # Regravar tecidos
        for tid, area in area_tecs.items():
            db.adicionar_tecido_na_peca(peca_id, tid, area)

        st.success("Peça atualizada! Atualize a página.")


if edit_mode and col2.button("🗑️ Excluir Peça"):
    db.excluir_peca(peca_id)
    st.warning("Peça excluída! Atualize a página.")


# ------------------------------------------
# Exibir custo detalhado da peça
# ------------------------------------------
if edit_mode:
    st.divider()
    st.subheader("📊 Detalhamento de Custos da Peça")

    custos = db.compute_peca_cost(peca_id)

    if custos:
        st.write(f"**Materiais:** R$ {custos['custo_materiais']:.2f}")
        st.write(f"**Tecidos:** R$ {custos['custo_tecidos']:.2f}")
        st.write(f"**Mão de Obra:** R$ {custos['custo_mao_de_obra']:.2f}")
        st.write(f"**Custo Total:** R$ {custos['custo_total']:.2f}")

        st.markdown(f"## 💰 **Preço Sugerido: R$ {custos['preco_sugerido']:.2f}**")

        if st.button("Salvar preço sugerido na peça"):
            db.salvar_preco_sugerido(peca_id, custos["preco_sugerido"])
            st.success("Preço sugerido atualizado!")
