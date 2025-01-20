import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# Configurar a página
st.set_page_config(page_title="Relatório de Trabalho", layout="wide")

# Título e descrição
st.title("Relatório de Trabalho")
st.markdown("Bem-vindo ao painel de resultados e progresso. Aqui você encontrará as principais informações sobre as tarefas, progresso e atualizações.")

# 1. Apresentação Geral
st.header("Apresentação Geral")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Tarefas Concluídas", value=15, delta="+3 desde ontem")
with col2:
    st.metric(label="Tarefas Pendentes", value=8, delta="-2 desde ontem")
with col3:
    st.metric(label="Progresso Geral (%)", value="75%", delta="+5%")

# 2. Tabela de Tarefas
st.header("Tabela de Tarefas")
tasks = {
    "Tarefa": ["Analisar dados", "Revisar relatório", "Implementar função", "Testar funcionalidades"],
    "Responsável": ["João", "Maria", "Ana", "Carlos"],
    "Status": ["Concluído", "Em andamento", "Pendente", "Em andamento"],
    "Prazo": ["2025-01-18", "2025-01-20", "2025-01-22", "2025-01-25"]
}
df_tasks = pd.DataFrame(tasks)
st.dataframe(df_tasks)

# 3. Progresso por Tarefa
st.header("Progresso por Tarefa")
progress = {
    "Tarefa": ["Analisar dados", "Revisar relatório", "Implementar função", "Testar funcionalidades"],
    "Progresso (%)": [100, 50, 20, 40]
}
df_progress = pd.DataFrame(progress)

# Gráfico de barras interativo com Plotly
fig = px.bar(
    df_progress,
    x="Tarefa",
    y="Progresso (%)",
    title="Progresso das Tarefas",
    labels={"Progresso (%)": "Progresso (%)", "Tarefa": "Tarefas"},
    text="Progresso (%)",
    color="Progresso (%)",
    color_continuous_scale="Blues"
)

fig.update_traces(texttemplate='%{text}%', textposition='outside')
fig.update_layout(
    xaxis_title="Tarefas",
    yaxis_title="Progresso (%)",
    showlegend=False,
    height=500
)

st.plotly_chart(fig)

# 4. Novidades e Atualizações
st.header("Novidades e Atualizações")
st.text_area("Anotações", placeholder="Digite aqui as novidades ou atualizações recentes...")

# Rodapé
st.markdown("---")
st.markdown("**Relatório gerado com Streamlit**")
