import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ========== CONFIGURAÇÃO DA PÁGINA ==========
st.set_page_config(
    page_title="Painel de Exportações",
    page_icon="🌎",
    layout="wide"
)

# ========== TÍTULO ==========
st.markdown("""
    <h1 style='font-size: 2.5rem; color: #1f77b4;'>📊 Painel de Inteligência de Exportações</h1>
    <p style='color: #555;'>Visualização moderna e interativa com dados de exportação.</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ========== SIMULAÇÃO DE DADOS ==========
@st.cache_data
def carregar_dados():
    dados = {
        "País": ["Brasil", "EUA", "China", "Alemanha", "Argentina", "Brasil", "EUA", "China"],
        "Produto": ["Milho", "Soja", "Café", "Carne", "Milho", "Soja", "Café", "Carne"],
        "Valor_FOB_USD": [10000, 15000, 13000, 9000, 7000, 12000, 14000, 8000],
        "Quantidade": [400, 500, 300, 200, 100, 350, 450, 180],
        "Ano": [2022, 2022, 2022, 2022, 2023, 2023, 2023, 2023]
    }
    return pd.DataFrame(dados)

df = carregar_dados()

# ========== BARRA LATERAL DE FILTROS ==========
with st.sidebar:
    st.header("📁 Filtros")
    anos = sorted(df["Ano"].unique())
    ano_selecionado = st.selectbox("Selecione o Ano", options=anos)

    paises = ["Todos"] + sorted(df["País"].unique())
    pais_selecionado = st.selectbox("Selecione o País", options=paises)

# ========== APLICAR FILTROS ==========
df_filtrado = df[df["Ano"] == ano_selecionado]
if pais_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["País"] == pais_selecionado]

# ========== KPIs ==========
col1, col2, col3 = st.columns(3)

col1.metric("💰 Valor Exportado (US$)", f"${df_filtrado['Valor_FOB_USD'].sum():,.0f}")
col2.metric("📦 Quantidade Total", f"{df_filtrado['Quantidade'].sum():,.0f}")
col3.metric("📈 Produtos Exportados", df_filtrado["Produto"].nunique())

st.markdown("---")

# ========== GRÁFICO BARRA ==========
st.subheader("📌 Exportações por Produto")
grafico_barra = px.bar(df_filtrado, x="Produto", y="Valor_FOB_USD",
                       color="Produto", text_auto=".2s",
                       labels={"Valor_FOB_USD": "Valor (US$)"},
                       height=400)
grafico_barra.update_layout(showlegend=False)
st.plotly_chart(grafico_barra, use_container_width=True)

# ========== GRÁFICO PIZZA ==========
st.subheader("🧭 Distribuição por País")
df_pizza = df_filtrado.groupby("País")["Valor_FOB_USD"].sum().reset_index()
grafico_pizza = px.pie(df_pizza, names="País", values="Valor_FOB_USD", hole=0.4)
grafico_pizza.update_traces(textinfo="percent+label")
st.plotly_chart(grafico_pizza, use_container_width=True)

# ========== TABELA ==========
st.markdown("### 📄 Dados detalhados")
st.dataframe(df_filtrado.reset_index(drop=True))
