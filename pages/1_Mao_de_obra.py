import streamlit as st
import database as db

st.set_page_config(page_title="Mão de Obra - Calculadora de Orçamento", layout="wide")

st.title("👷🏽‍♂️ Configuração de Mão de Obra")
st.write("Defina o valor da sua hora trabalhada e a margem de lucro. Isso será usado automaticamente no cálculo do preço sugerido de cada peça.")

# -----------------------------------------------------
# Carregar configurações atuais
# -----------------------------------------------------
cfg = db.carregar_configuracoes()
valor_hora_atual = cfg["valor_hora"]
margem_atual = cfg["margem"]

st.subheader("Valores Atuais")
colA, colB = st.columns(2)
colA.metric("Valor da Hora (R$)", f"R$ {valor_hora_atual:,.2f}")
colB.metric("Margem de Lucro (%)", f"{margem_atual:.1f}%")

st.divider()

# -----------------------------------------------------
# Formulário para atualizar as configurações
# -----------------------------------------------------
st.subheader("Atualizar Configurações")

with st.form("form_mao_obra", clear_on_submit=False):
    novo_valor_hora = st.number_input(
        "Valor da hora trabalhada (R$)",
        min_value=0.0,
        step=1.0,
        value=float(valor_hora_atual)
    )

    nova_margem = st.number_input(
        "Margem de lucro (%)",
        min_value=0.0,
        step=1.0,
        value=float(margem_atual)
    )

    salvar = st.form_submit_button("Salvar Configurações")

if salvar:
    db.salvar_configuracoes(novo_valor_hora, nova_margem)
    st.success("Configurações atualizadas com sucesso!")
    st.rerun()

st.markdown("---")
st.caption("As configurações acima serão aplicadas automaticamente em todos os cálculos de peças.")
