import streamlit as st
import pandas as pd
from database import (
    listar_tecidos,
    inserir_tecido,
    atualizar_tecido,
    excluir_tecido,
    nome_tecido_existe
)

st.set_page_config(page_title="Tecidos", layout="wide")

st.title("🧵 Gerenciamento de Tecidos")
st.write("Cadastre, edite e exclua tecidos utilizados na produção das peças.")

st.divider()

# ========================================================
# 🔄 Carregar tecidos em DataFrame
# ========================================================
tecidos = listar_tecidos()
df = pd.DataFrame(tecidos, columns=[
    "ID", "Nome", "Comprimento total (cm)", "Largura total (cm)", "Custo (R$)"
])

# ========================================================
# 📋 Exibir tabela de tecidos
# ========================================================
st.subheader("📦 Tecidos cadastrados")

if df.empty:
    st.info("Nenhum tecido cadastrado ainda.")
else:
    st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# ========================================================
# ➕ Cadastro de novo tecido
# ========================================================
st.subheader("➕ Cadastrar novo tecido")

with st.form("form_novo_tecido"):
    nome_tecido = st.text_input("Nome do tecido").strip()

    comprimento_total = st.number_input(
        "Comprimento total adquirido (cm)",
        min_value=1.0,
        step=1.0,
        format="%.1f"
    )

    largura_total = st.number_input(
        "Largura total adquirida (cm)",
        min_value=1.0,
        step=1.0,
        format="%.1f"
    )

    custo = st.number_input(
        "Custo total (R$)",
        min_value=0.0,
        step=1.0,
        format="%.2f"
    )

    submit_novo = st.form_submit_button("Cadastrar tecido")

if submit_novo:
    if not nome_tecido:
        st.error("O nome do tecido é obrigatório.")
    elif nome_tecido_existe(nome_tecido):
        st.error("Já existe um tecido com este nome.")
    else:
        inserir_tecido(nome_tecido, comprimento_total, largura_total, custo)
        st.success("Tecido cadastrado com sucesso! 🎉")
        st.rerun()

st.divider()

# ========================================================
# ✏️ Editar tecido existente
# ========================================================
st.subheader("✏️ Editar tecido")

if df.empty:
    st.info("Cadastre um tecido primeiro.")
else:
    tecido_escolhido = st.selectbox(
        "Selecione o tecido para editar",
        df["Nome"].tolist()
    )

    dados = df[df["Nome"] == tecido_escolhido].iloc[0]
    id_t = int(dados["ID"])

    with st.form("form_editar_tecido"):
        novo_nome = st.text_input("Nome do tecido", value=dados["Nome"]).strip()

        novo_comprimento = st.number_input(
            "Comprimento total adquirido (cm)",
            min_value=1.0,
            step=1.0,
            value=float(dados["Comprimento total (cm)"]),
            format="%.1f"
        )

        nova_largura = st.number_input(
            "Largura total adquirida (cm)",
            min_value=1.0,
            step=1.0,
            value=float(dados["Largura total (cm)"]),
            format="%.1f"
        )

        novo_custo = st.number_input(
            "Custo total (R$)",
            min_value=0.0,
            step=1.0,
            value=float(dados["Custo (R$)"]),
            format="%.2f"
        )

        submit_edit = st.form_submit_button("Salvar alterações")

    if submit_edit:
        if not novo_nome:
            st.error("O nome do tecido é obrigatório.")
        elif novo_nome != dados["Nome"] and nome_tecido_existe(novo_nome):
            st.error("Já existe um tecido com este nome.")
        else:
            atualizar_tecido(id_t, novo_nome, novo_comprimento, nova_largura, novo_custo)
            st.success("Tecido atualizado com sucesso! ✨")
            st.rerun()

st.divider()

# ========================================================
# 🗑 Excluir tecido
# ========================================================
st.subheader("🗑 Excluir tecido")

if df.empty:
    st.info("Cadastre um tecido primeiro.")
else:
    tecido_excluir = st.selectbox(
        "Selecione o tecido para excluir",
        df["Nome"].tolist(),
        key="excluir_tecido"
    )

    id_excluir = int(df[df["Nome"] == tecido_excluir]["ID"].iloc[0])

    if st.button("Excluir tecido", type="primary", use_container_width=True):
        excluir_tecido(id_excluir)
        st.success("Tecido excluído com sucesso! 🗑️")
        st.rerun()
