import streamlit as st
import streamlit.components.v1 as components

def main():
    st.title('Hello, World!')
    st.write('Este é um exemplo básico de aplicação Streamlit.')

    # Barra Lateral
    st.sidebar.title('Configurações')
    # Campo de texto
    user_input = st.sidebar.text_input('Digite algo:', 'Hello, Streamlit!')
     # Controle deslizante
    slider_value = st.sidebar.slider('Escolha um valor:', 0, 100, 50)
    # Caixa de seleção
    checkbox = st.sidebar.checkbox('Marque esta caixa')
    # Área Principal
    st.write('Você digitou:', user_input)
    st.write('Valor selecionado no slider:', slider_value)
    st.write('Checkbox marcado:', checkbox)


    # HTML e JavaScript para criar um botão com ação
    html_code = f"""
    <html>
        <head>
            <style>
                .custom-box {{
                    background-color: #f0f8ff;
                    padding: 20px;
                    border-radius: 10px;
                    border: 1px solid #ccc;
                }}
                .custom-button {{
                    background-color: #ff4500;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    border: none;
                    cursor: pointer;
                }}
            </style>
        </head>
        <body>
            <div class="custom-box">
                <h1>Caixa Personalizada</h1>
                <p>Texto de entrada: {user_input}</p>
                <p id="result"></p>
            </div>
        </body>
    </html>
    """

    # Renderiza o HTML personalizado
    components.html(html_code, height=300, scrolling=True)

    # Manipula a mensagem recebida no Streamlit
    message = st.experimental_get_query_params().get('message', [''])[0]
    if message == 'button_click':
        st.write("Botão clicado!")

    

if __name__ == "__main__":
    main()
