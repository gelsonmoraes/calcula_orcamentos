import streamlit as st

#Congfiguração da página principal
st.set_page_config(page_title="Calculadora de Orçamento", layout="wide")
st.title("Calculadora de Orçamento")

# Inicia banco de dados
# init_db()

#Definição das páginas

mao_de_obra = st.Page("pages/2_Mao_de_Obra.py", title="Mão de Obra", icon="👷🏾")
materiais = st.Page("pages/3_Materiais.py", title="Materiais", icon="🧱")
tecidos = st.Page("pages/4_Tecidos.py", title="Tecidos", icon="🧵")
pecas = st.Page("pages/5_Pecas.py", title="Peças", icon="🧩")

pg = st.navigation(pages=[mao_de_obra, materiais, tecidos, pecas])
st.sidebar.caption("Calculadora de Orçamento")

st.write("Selecione uma página no menu lateral para começar.")
pg.run()