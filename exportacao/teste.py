import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards

# ============ CONFIGURAÇÃO DA PÁGINA ============
st.set_page_config(page_title="Painel de Exportações", layout="wide")
# st.set_page_config(page_title=None, page_icon=None, layout=None, initial_sidebar_state=None, menu_items=None)

st.markdown("""
    <style>
        .metric-label > div {
            font-size: 20px;
        }
        .stMetric {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 0 4px rgba(0,0,0,0.05);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# ============ CARREGAMENTO DOS DADOS ============
@st.cache_data
def carregar_dados():
    return pd.read_csv("./data/dados_exportacao_transformado.csv")

df = carregar_dados()

# ============ FILTROS ============
st.sidebar.header("🔎 Filtros")

anos = sorted(df["Ano"].unique(), reverse=True)
ncm_opcoes = df["Código NCM"].unique()
paises_opcoes = df["Países"].unique()

ano = st.sidebar.selectbox("Selecione o Ano", anos)
ncm_selecionados = st.sidebar.multiselect("Códigos NCM", ncm_opcoes, default=ncm_opcoes[:3])
paises_selecionados = st.sidebar.multiselect("Países", paises_opcoes, default=paises_opcoes[:3])

df_filtrado = df[
    (df["Ano"] == ano) &
    (df["Código NCM"].isin(ncm_selecionados)) &
    (df["Países"].isin(paises_selecionados))
]

# # ============ TÍTULO ============
# st.title("📊 Painel de Inteligência de Exportações")
# st.markdown(f"### 📅 Análise do Ano **{ano}** com base nos produtos e países selecionados")


# # ============ KPIs ============
# col1, col2, col3 = st.columns(3)

# col1.metric("💰 Valor Exportado (US$)", f"${df_filtrado['Valor_FOB_USD'].sum():,.0f}")
# col2.metric("⚖️ Peso Total (kg)", f"{df_filtrado['Peso_Kg'].sum():,.0f}")
# col3.metric("📦 Quantidade Total", f"{df_filtrado['Quantidade'].sum():,.0f}")

# st.markdown("---")

# ============ TÍTULO BONITO ============
st.markdown("""
    <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1f77b4;
            margin-bottom: 0.3rem;
        }
        .subtitle {
            font-size: 1.3rem;
            color: #444;
        }
        .kpi-card {
            background: linear-gradient(135deg, #f0f9ff, #dbefff);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .kpi-title {
            font-size: 1.1rem;
            color: #333;
            margin-bottom: 5px;
        }
        .kpi-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #1f77b4;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="main-title">📊 Painel de Inteligência de Exportações</div>
    <div class="subtitle">📅 Análise do Ano <strong>{ano}</strong> com base nos produtos e países selecionados</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============ KPIs COM ESTILO ============
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">💰 Valor Exportado (US$)</div>
            <div class="kpi-value">${df_filtrado['Valor_FOB_USD'].sum():,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">⚖️ Peso Total (kg)</div>
            <div class="kpi-value">{df_filtrado['Peso_Kg'].sum():,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">📦 Quantidade Total</div>
            <div class="kpi-value">{df_filtrado['Quantidade'].sum():,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")


# ============ DESTAQUES DE EXPORTAÇÃO ============
st.set_page_config(layout="wide")

st.markdown("## 🏆 Destaques de Exportação")

# Estilização CSS leve
st.markdown("""
<style>
.metric-container {
    background: linear-gradient(135deg, #c2e9fb, #a1c4fd);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    animation: pulse 2s infinite;
}
.metric-title {
    font-size: 1.1rem;
    color: #333;
}
.metric-value {
    font-size: 2rem;
    font-weight: bold;
    margin-top: 5px;
}
@keyframes pulse {
  0% {box-shadow: 0 0 0 0 rgba(0,123,255, 0.4);}
  70% {box-shadow: 0 0 0 10px rgba(0,123,255, 0);}
  100% {box-shadow: 0 0 0 0 rgba(0,123,255, 0);}
}
</style>
""", unsafe_allow_html=True)

# Agrupamentos dos dados
pais_top = df_filtrado.groupby("Países")["Valor_FOB_USD"].sum().reset_index() \
                      .sort_values(by="Valor_FOB_USD", ascending=False).head(1)

ncm_top = df_filtrado.groupby(["Código NCM", "Descrição NCM"])["Quantidade"].sum().reset_index() \
                     .sort_values(by="Quantidade", ascending=False).head(1)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        if not pais_top.empty:
            pais = pais_top.iloc[0]["Países"]
            valor = pais_top.iloc[0]["Valor_FOB_USD"]
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-title">🌍 País com Maior Valor Exportado</div>
                <div class="metric-value">{pais}</div>
                <div>💰 US$ {valor:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if not ncm_top.empty:
            ncm = ncm_top.iloc[0]["Código NCM"]
            desc = ncm_top.iloc[0]["Descrição NCM"]
            qtd = ncm_top.iloc[0]["Quantidade"]
            st.markdown(f"""
            <div class="metric-container" style="background: linear-gradient(135deg, #fbc2eb, #a6c1ee);">
                <div class="metric-title">📦 Produto Mais Exportado</div>
                <div class="metric-value">NCM {ncm}</div>
                <div>{desc}</div>
                <div>📦 {int(qtd):,} unidades</div>
            </div>
            """, unsafe_allow_html=True)

# # Gráfico complementar interativo com Plotly
# st.markdown("### 📈 Top 5 Países por Valor Exportado")

# top5_paises = df_filtrado.groupby("Países")["Valor_FOB_USD"].sum() \
#                          .sort_values(ascending=False).head(5).reset_index()

# fig = px.bar(top5_paises, x="Países", y="Valor_FOB_USD",
#              color="Países", text_auto=".2s",
#              title="Top 5 Destinos das Exportações",
#              labels={"Valor_FOB_USD": "Valor (US$)"},
#              height=400)

# fig.update_layout(showlegend=False)
# st.plotly_chart(fig, use_container_width=True)
            
# === Filtro de Países ===
paises_disponiveis = df_filtrado["Países"].dropna().unique().tolist()
paises_disponiveis.sort()
opcao_pais = st.selectbox("🌍 Filtrar por País", options=["Todos"] + paises_disponiveis)

# === Aplicar Filtro ===
if opcao_pais == "Todos":
    df_top = df_filtrado.copy()
else:
    df_top = df_filtrado[df_filtrado["Países"] == opcao_pais]

# === Cálculo dos Top 5 países ===
top5_paises = (
    df_top.groupby("Países")["Valor_FOB_USD"]
    .sum()
    .reset_index()
)

# Se estiver filtrando por 1 país, garantir que ainda traga top 5 do total
if opcao_pais == "Todos":
    top5_paises = top5_paises.sort_values(by="Valor_FOB_USD", ascending=False).head(5)
else:
    # Força exibição de 5 países: adiciona extras se necessário
    top5_completos = (
        df_filtrado.groupby("Países")["Valor_FOB_USD"]
        .sum()
        .reset_index()
        .sort_values(by="Valor_FOB_USD", ascending=False)
        .head(5)
    )
    top5_paises = pd.concat([top5_paises, top5_completos]).drop_duplicates(subset=["Países"]).head(5)

# === Gráfico com Plotly ===
st.markdown("### 📈 Top 5 Países por Valor Exportado")

if not top5_paises.empty:
    fig = px.bar(top5_paises, x="Países", y="Valor_FOB_USD",
                 color="Países", text_auto=".2s",
                 title="Top 5 Destinos das Exportações",
                 labels={"Valor_FOB_USD": "Valor (US$)"},
                 height=400)
    fig.update_layout(showlegend=False)
    fig.update_traces(marker_line_width=1.5, marker_line_color='black')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ Nenhum dado disponível para o país selecionado.")




# ============ GRÁFICO - VALOR POR PAÍS ============
st.subheader("🌍 Valor Exportado por País")
df_valor_pais = df_filtrado.groupby("Países")["Valor_FOB_USD"].sum().reset_index()
fig_pais = px.bar(df_valor_pais.sort_values("Valor_FOB_USD", ascending=False),
                  x="Valor_FOB_USD", y="Países",
                  orientation="h", text_auto=".2s",
                  labels={"Valor_FOB_USD": "US$ FOB", "Países": "País"},
                  title="Top Países por Valor Exportado")
fig_pais.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=400)
st.plotly_chart(fig_pais, use_container_width=True)

# ============ GRÁFICO - VALOR POR NCM ============
st.subheader("📦 Valor Exportado por Código NCM")
df_valor_ncm = df_filtrado.groupby("Código NCM")["Valor_FOB_USD"].sum().reset_index()
fig_ncm = px.bar(df_valor_ncm.sort_values("Valor_FOB_USD", ascending=False),
                 x="Código NCM", y="Valor_FOB_USD", text_auto=".2s",
                 labels={"Valor_FOB_USD": "US$ FOB"},
                 title="Top Produtos Exportados (NCM)")
fig_ncm.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=400)
st.plotly_chart(fig_ncm, use_container_width=True)

# ============ EVOLUÇÃO HISTÓRICA ============
st.subheader("📈 Evolução Anual (Todos os anos)")
df_evolucao = df[
    (df["Código NCM"].isin(ncm_selecionados)) &
    (df["Países"].isin(paises_selecionados))
].groupby("Ano")["Valor_FOB_USD"].sum().reset_index()

fig_evol = px.line(df_evolucao, x="Ano", y="Valor_FOB_USD", markers=True,
                   labels={"Valor_FOB_USD": "US$ FOB"},
                   title="Evolução Histórica das Exportações")
fig_evol.update_traces(line=dict(width=3))
st.plotly_chart(fig_evol, use_container_width=True)

# ============ TABELA ============
st.subheader("📋 Tabela Detalhada")
st.dataframe(df_filtrado.sort_values(by="Valor_FOB_USD", ascending=False),
             use_container_width=True, height=400)
