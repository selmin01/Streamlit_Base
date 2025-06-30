import streamlit as st
import plotly.graph_objs as go
import numpy as np

# Estilo inicial
st.set_page_config(page_title="Educação Financeira", layout="wide")

# Título e cabeçalho
st.title("💰 Educação Financeira Interativa")
st.subheader("Gerencie suas finanças com aprendizado prático e visualizações modernas!")

# Menu lateral
menu = st.sidebar.radio(
    "Navegue pelas opções:",
    ["Introdução", "Calculadora de Juros Compostos", "Orçamento Pessoal", "Simulação de Investimentos", "Dicas de Finanças"]
)

if menu == "Introdução":
    st.header("📚 Conceitos básicos de finanças pessoais")
    st.markdown("""
    - **Orçamento:** Entender suas receitas e despesas é o ponto inicial.
    - **Juros compostos:** Aprenda como o dinheiro pode crescer exponencialmente.
    - **Investimentos:** Conheça opções para fazer o dinheiro trabalhar para você.
    """)

elif menu == "Calculadora de Juros Compostos":
    st.header("📈 Calculadora de Juros Compostos")

    # Inputs do usuário
    principal = st.number_input("Investimento inicial (R$)", min_value=0.0, value=1000.0, step=100.0)
    rate = st.slider("Taxa de juros anual (%)", 0.0, 20.0, 5.0)
    time = st.slider("Duração (anos)", 1, 30, 10)

    # Cálculo do montante final
    final_amount = principal * ((1 + (rate / 100)) ** time)
    st.write(f"💰 Montante final após {time} anos: **R${final_amount:,.2f}**")

    # Dados para o gráfico
    anos = np.arange(1, time + 1)
    montantes = principal * ((1 + (rate / 100)) ** anos)

    # Gráfico usando Plotly
    fig = go.Figure(
        go.Scatter(
            x=anos,
            y=montantes,
            mode="lines+markers",
            line=dict(color="#2A9D8F", width=3),
            marker=dict(size=8),
            name="Crescimento"
        )
    )
    fig.update_layout(
        title="Evolução do Investimento",
        xaxis_title="Anos",
        yaxis_title="Montante acumulado (R$)",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Orçamento Pessoal":
    st.header("💸 Planeje seu orçamento")
    receita = st.number_input("Receita mensal (R$)", min_value=0.0, value=5000.0)

    despesas = {
        "Moradia": st.number_input("Gasto com moradia (R$)", min_value=0.0, value=1500.0),
        "Alimentação": st.number_input("Gasto com alimentação (R$)", min_value=0.0, value=800.0),
        "Transporte": st.number_input("Gasto com transporte (R$)", min_value=0.0, value=500.0),
        "Lazer": st.number_input("Gasto com lazer (R$)", min_value=0.0, value=300.0),
        "Outros": st.number_input("Outras despesas (R$)", min_value=0.0, value=200.0),
    }

    total_despesas = sum(despesas.values())
    saldo = receita - total_despesas

    st.write(f"📊 Total de despesas: **R${total_despesas:,.2f}**")
    st.write(f"💵 Saldo final: **R${saldo:,.2f}**")

    # Gráfico de pizza usando Plotly
    fig = go.Figure(
        go.Pie(
            labels=list(despesas.keys()),
            values=list(despesas.values()),
            hole=0.3,
            marker=dict(colors=["#e63946", "#f4a261", "#2a9d8f", "#264653", "#e76f51"]),
        )
    )
    fig.update_layout(title="Distribuição do orçamento")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Simulação de Investimentos":
    st.header("📊 Simule o crescimento de um investimento")

    # Inputs do usuário
    investimento_inicial = st.number_input("Valor inicial (R$)", min_value=0.0, value=1000.0)
    aportes_mensais = st.number_input("Aportes mensais (R$)", min_value=0.0, value=200.0)
    taxa_anual = st.slider("Taxa de juros anual (%)", 0.0, 20.0, 8.0)
    anos = st.slider("Duração do investimento (anos)", 1, 30, 10)

    # Simulação do crescimento
    saldo_acumulado = [investimento_inicial]
    for i in range(anos * 12):
        novo_saldo = saldo_acumulado[-1] * (1 + (taxa_anual / 100) / 12) + aportes_mensais
        saldo_acumulado.append(novo_saldo)

    # Gráfico usando Plotly
    meses = np.arange(0, len(saldo_acumulado))
    fig = go.Figure(
        go.Scatter(
            x=meses,
            y=saldo_acumulado,
            mode="lines",
            line=dict(color="#FF5733", width=3),
            name="Saldo acumulado"
        )
    )
    fig.update_layout(
        title="Evolução do investimento com aportes mensais",
        xaxis_title="Meses",
        yaxis_title="Saldo acumulado (R$)",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Dicas de Finanças":
    st.header("💡 Dicas para gerenciar suas finanças pessoais")
    st.write("""
    - **Controle seus gastos:** Registre todas as despesas e receitas.
    - **Poupança automática:** Configure transferências automáticas para poupança ou investimentos.
    - **Diversifique seus investimentos:** Não coloque todo o seu dinheiro em uma única aplicação.
    - **Eduque-se:** Estude constantemente sobre finanças para tomar decisões melhores.
    """)
    st.write("🔗 [Saiba mais](https://www.meubolsoemdia.com.br/)")

