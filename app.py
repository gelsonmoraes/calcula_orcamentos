import streamlit as st

#Congfiguração da página principal
st.set_page_config(page_title="Calculadora de Orçamento", layout="wide")

# Inicia banco de dados
# init_db()

#Definição das páginas

mao_de_obra = st.Page("pages/1_Mao_de_obra.py", title="Mão de Obra", icon="👷🏾")
materiais = st.Page("pages/2_Materiais.py", title="Materiais", icon="🧱")
tecidos = st.Page("pages/3_Tecidos.py", title="Tecidos", icon="🧵")
pecas = st.Page("pages/4_Pecas.py", title="Peças", icon="🧩")

pg = st.navigation(pages=[mao_de_obra, materiais, tecidos, pecas])
st.sidebar.caption("Calculadora de Orçamento")

pg.run()