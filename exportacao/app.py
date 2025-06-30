import streamlit as st
import pandas as pd
import plotly.express as px
from babel.numbers import format_currency, format_decimal

@st.cache_data
def carregar_dados():
    return pd.read_csv("./data/dados_exportacao_transformado.csv")

# Carrega os dados
df = carregar_dados()
df.columns = df.columns.str.strip()  # remove espaços extras
# st.write("🧾 Colunas disponíveis:", df.columns.tolist())

# ========== CONFIGURAÇÃO DA PÁGINA ==========
st.set_page_config(
    page_title="Painel de Exportações",
    page_icon="🌎",
    layout="wide"
)

# ========== FILTROS NA SIDEBAR ==========
with st.sidebar:
    st.header("📁 Filtros de Exportação")

    # ====== FILTRO DE ANOS ======
    anos_disponiveis = sorted(df["Ano"].unique(), reverse=True)
    opcoes_ano = ["Todos os anos"] + anos_disponiveis

    anos_escolhidos = st.multiselect(
        "📅 Selecione os Anos",
        options=opcoes_ano,
        default=["Todos os anos"]
    )

    if "Todos os anos" in anos_escolhidos or not anos_escolhidos:
        anos_selecionados = anos_disponiveis
    else:
        anos_selecionados = anos_escolhidos

    # ====== FILTRO DE PAÍSES ======
    paises_disponiveis = sorted(df["Países"].unique())
    opcoes_pais = ["Todos os países"] + paises_disponiveis

    paises_escolhidos = st.multiselect(
        "🌍 Selecione os Países",
        options=opcoes_pais,
        default=["Todos os países"]
    )

    if "Todos os países" in paises_escolhidos or not paises_escolhidos:
        paises_selecionados = paises_disponiveis
    else:
        paises_selecionados = paises_escolhidos

df_filtrado = df[
    (df["Ano"].isin(anos_selecionados)) &
    (df["Países"].isin(paises_selecionados))
]
# ////////////////////////////,,////////////////////////////
#
#
#
#
# ////////////////////////////,,////////////////////////////


# ========== TÍTULO ==========
st.markdown("""
    <h1 style='font-size: 2.5rem; color: #1f77b4;'>📊 Painel de Inteligência de Exportações</h1>
    <p style='color: #555;'>Visualização moderna e interativa com dados de exportação.</p>
""", unsafe_allow_html=True)
# st.markdown("---")


# ============ ESTILO CSS PARA KPI CARDS ============
st.markdown("""
    <style>
        .kpi-card {
            background: linear-gradient(135deg, #f0f4f8, #ffffff);
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            text-align: center;
            transition: all 0.3s ease-in-out;
            border: 1px solid #e0e0e0;
        }
        .kpi-card:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        }
        .kpi-title {
            font-size: 1.1rem;
            color: #333;
            margin-bottom: 6px;
        }
        .kpi-value {
            font-size: 2rem;
            font-weight: 700;
            color: #1f77b4;
        }
    </style>
""", unsafe_allow_html=True)

# ============ KPIs COM ESTILO + COLUNAS ============
valor_total = format_currency(df_filtrado["Valor_FOB_USD"].sum(), 'USD', locale='en_US')
peso_total = format_decimal(df_filtrado["Peso_Kg"].sum(), locale='pt_BR')
quantidade_total = format_decimal(df_filtrado["Quantidade"].sum(), locale='pt_BR')

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">💰 Valor Exportado (US$)</div>
            <div class="kpi-value">{valor_total}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">⚖️ Peso Total (kg)</div>
            <div class="kpi-value">{peso_total}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">📦 Quantidade Total</div>
            <div class="kpi-value">{quantidade_total}</div>
        </div>
    """, unsafe_allow_html=True)


st.markdown(f"""
        <br></br>
    """, unsafe_allow_html=True)

# Divide a tela em duas colunas: 50% / 50%
coluna1, coluna2 = st.columns([2,3.5])

with coluna1:
    st.markdown("#### 🗂️ Tabela de Exportações")
    st.dataframe(df, use_container_width=True, height=300)

with coluna2:
    # Gráfico de participação percentual por país
    df_participacao = df_filtrado.groupby("Países")["Valor_FOB_USD"].sum().reset_index()
    df_participacao["% Participação"] = (
        df_participacao["Valor_FOB_USD"] / df_participacao["Valor_FOB_USD"].sum()
    ) * 100

    # Ordenar e manter os 8 principais + "Outros"
    top_paises = df_participacao.sort_values(by="% Participação", ascending=False)
    if len(top_paises) > 8:
        top = top_paises.head(8)
        outros = pd.DataFrame({
            "Países": ["Outros"],
            "Valor_FOB_USD": [top_paises.iloc[8:]["Valor_FOB_USD"].sum()],
            "% Participação": [top_paises.iloc[8:]["% Participação"].sum()]
        })
        df_plot = pd.concat([top, outros])
    else:
        df_plot = top_paises

    # Criar o gráfico
    fig = px.pie(
        df_plot,
        names="Países",
        values="Valor_FOB_USD",
        title="Participação nas Exportações ",
        hole=0.3
    )

    fig.update_traces(textinfo='percent+label')
    fig.update_layout(
        title_font_size=20,
        title_x=0.45,
        showlegend=True
    )

    # Exibir no app
    st.plotly_chart(fig, use_container_width=True)



# ============ INDICADORES AVANÇADOS ============
st.markdown("---")
st.markdown("## Indicadores Avançados de Exportação")

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Crescimento Médio Anual",
    "💳 Ticket Médio por Tonelada",
    "🌍 Participação por País",
    "🔥 Produtos com Maior Valor FOB/Peso"
])

# 1. Crescimento médio anual por país e NCM
with tab1:
    st.markdown("### 📈 Crescimento médio anual por país e NCM")
    df_crescimento = df_filtrado.groupby(["Ano", "Países", "Código NCM"])["Valor_FOB_USD"].sum().reset_index()
    df_crescimento = df_crescimento.sort_values(by=["Países", "Código NCM", "Ano"])
    df_crescimento["Crescimento (%)"] = df_crescimento.groupby(["Países", "Código NCM"])["Valor_FOB_USD"].pct_change() * 100
    df_crescimento_medio = df_crescimento.groupby(["Países", "Código NCM"])["Crescimento (%)"].mean().reset_index()
    st.dataframe(df_crescimento_medio, use_container_width=True)

# 2. Ticket médio por tonelada
with tab2:
    st.markdown("### 💳 Ticket médio por tonelada (US$/kg)")
    df_ticket_medio = df_filtrado.groupby("Países").apply(
        lambda x: x["Valor_FOB_USD"].sum() / x["Peso_Kg"].sum()
    ).reset_index(name="Ticket Médio (US$/kg)")
    st.dataframe(df_ticket_medio, use_container_width=True)

# 3. Participação percentual por país
with tab3:
    st.markdown("### 🌍 Participação percentual de cada país nas exportações")
    df_participacao = df_filtrado.groupby("Países")["Valor_FOB_USD"].sum().reset_index()
    df_participacao["% Participação"] = (
        df_participacao["Valor_FOB_USD"] / df_participacao["Valor_FOB_USD"].sum()
    ) * 100
    st.dataframe(df_participacao.sort_values(by="% Participação", ascending=False), use_container_width=True)

# 4. Produtos com maior relação valor FOB / peso
with tab4:
    st.markdown("### 🔥 Produtos com maior relação Valor FOB / Peso (kg)")
    df_relacao_valor_peso = df_filtrado.copy()
    df_relacao_valor_peso["Valor_por_Kg"] = df_relacao_valor_peso["Valor_FOB_USD"] / df_relacao_valor_peso["Peso_Kg"]
    df_top_valor_peso = df_relacao_valor_peso.groupby(["Código NCM", "Descrição NCM"])["Valor_por_Kg"].mean() \
        .reset_index().sort_values(by="Valor_por_Kg", ascending=False).head(10)
    st.dataframe(df_top_valor_peso, use_container_width=True)
