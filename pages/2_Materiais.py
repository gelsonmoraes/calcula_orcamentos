import streamlit as st
import pandas as pd
import database as db
from math import ceil
from io import StringIO

st.set_page_config(page_title="Materiais - Calculadora", layout="wide")
st.title("🧱 Materiais")
st.write("Gerencie os materiais usados nas peças — cadastre, edite, exclua e exporte.")

# ---------------------------
# Carregar e preparar dados
# ---------------------------
def carregar_df(busca: str = ""):
    rows = db.listar_materiais()
    if not rows:
        return pd.DataFrame(columns=["ID", "Nome", "Unidade", "Quantidade adquirida", "Custo (R$)"])
    df = pd.DataFrame(rows, columns=["ID", "Nome", "Unidade", "Quantidade adquirida", "Custo (R$)"])
    if busca:
        df = df[df["Nome"].str.contains(busca, case=False, na=False)]
    return df.reset_index(drop=True)

# ---------------------------
# Cabeçalho: pesquisa + export
# ---------------------------
col_search, col_page, col_export = st.columns([4, 2, 1])

with col_search:
    busca = st.text_input("Pesquisar por nome", "")

with col_page:
    page_size = st.selectbox("Itens por página", options=[5, 10, 20, 50], index=1)

with col_export:
    # export irá considerar o filtro de busca atual
    df_all = carregar_df(busca)
    csv_buf = df_all.to_csv(index=False, sep=",", decimal=".")
    st.download_button("Exportar CSV", data=csv_buf, file_name="materiais.csv", mime="text/csv")

st.divider()

# ---------------------------
# Paginação
# ---------------------------
df = carregar_df(busca)
total = len(df)
pages = max(1, ceil(total / page_size))
page_idx = st.number_input("Página", min_value=1, max_value=pages, value=1, step=1)

start = (page_idx - 1) * page_size
end = start + page_size
df_page = df.iloc[start:end]

st.markdown(f"**Mostrando {start+1} — {min(end, total)} de {total} materiais**")

# tabela simples
if df_page.empty:
    st.info("Nenhum material encontrado.")
else:
    df_page_display = df_page.drop(columns=["ID"])
    st.table(df_page_display.rename(columns={
        "Nome": "Nome",
        "Unidade": "Unidade",
        "Quantidade adquirida": "Qtd adquirida",
        "Custo (R$)": "Custo (R$)"
    }))


st.divider()

# ---------------------------
# Formulário: novo material
# ---------------------------
st.subheader("➕ Cadastrar novo material")

with st.form("novo_material"):
    nome = st.text_input("Nome do material", key="novo_nome").strip()
    unidade = st.selectbox("Unidade", ["metros", "centímetros", "quilogramas", "gramas", "mililitros", "litros", "peças"], key="novo_unidade")
    quantidade = st.number_input("Quantidade adquirida", min_value=0.0, step=0.1, format="%.2f", key="novo_qtd")
    custo = st.number_input("Custo total (R$)", min_value=0.0, step=0.1, format="%.2f", key="novo_custo")
    submit_novo = st.form_submit_button("Cadastrar material")

if submit_novo:
    if not nome:
        st.error("Nome é obrigatório.")
    elif db.nome_material_existe(nome):
        st.error("Já existe um material com esse nome.")
    else:
        db.inserir_material(nome, unidade, quantidade, custo)
        st.success("Material cadastrado com sucesso!")
        st.experimental_rerun()

st.divider()

# ---------------------------
# Formulário: editar material
# ---------------------------
st.subheader("✏️ Editar material")

df_full = carregar_df("")  # lista completa para escolher
if df_full.empty:
    st.info("Cadastre materiais antes de editar.")
else:
    nomes = {row["Nome"]: int(row["ID"]) for _, row in df_full.iterrows()}
    escolha = st.selectbox("Selecione material para editar", ["(nenhum)"] + list(nomes.keys()))
    if escolha != "(nenhum)":
        mid = nomes[escolha]
        # buscar detalhes
        row = df_full[df_full["ID"] == mid].iloc[0]
        with st.form("editar_material"):
            novo_nome = st.text_input("Nome", value=row["Nome"], key="edit_nome")
            nova_unidade = st.selectbox("Unidade", ["metros", "centímetros", "quilogramas", "gramas", "mililitros", "litros", "peças"], index=[
                "metros", "centímetros", "quilogramas", "gramas", "mililitros", "litros", "peças"
            ].index(row["Unidade"]))
            nova_qtd = st.number_input("Quantidade adquirida", min_value=0.0, step=0.1, value=float(row["Quantidade adquirida"]), format="%.2f")
            novo_custo = st.number_input("Custo total (R$)", min_value=0.0, step=0.1, value=float(row["Custo (R$)"]), format="%.2f")
            submit_edit = st.form_submit_button("Salvar alterações")

        if submit_edit:
            if not novo_nome:
                st.error("Nome é obrigatório.")
            elif novo_nome != row["Nome"] and db.nome_material_existe(novo_nome):
                st.error("Já existe outro material com esse nome.")
            else:
                db.atualizar_material(mid, novo_nome, nova_unidade, nova_qtd, novo_custo)
                st.success("Material atualizado com sucesso!")
                st.experimental_rerun()

        if st.button("🗑 Excluir material"):
            confirm = st.confirm("Tem certeza que deseja excluir este material? (A exclusão pode afetar peças que usem este material.)")
            if confirm:
                db.excluir_material(mid)
                st.warning("Material excluído.")
                st.experimental_rerun()

st.divider()

# ---------------------------
# Dicas e notas
# ---------------------------
with st.expander("Dicas"):
    st.write("""
    - Ao editar o nome de um material, o sistema valida duplicados.
    - Exporte CSV para integrar com planilhas ou backups.
    - Se você quiser paginação mais avançada (navegação por botões), posso implementar.
    """)
