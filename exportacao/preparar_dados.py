import pandas as pd

# Caminho do seu arquivo
caminho_arquivo = "../H_EXPORTACAO_GERAL_2020-01_2024-12_DT20250625.xlsx"

# Carregar a planilha
df = pd.read_excel(caminho_arquivo)

# Colunas fixas
id_vars = ['Países', 'Código NCM', 'Descrição NCM']

# Separar colunas por tipo de dado
valor_cols = [col for col in df.columns if 'Valor US$ FOB' in col]
peso_cols = [col for col in df.columns if 'Quilograma Líquido' in col]
quant_cols = [col for col in df.columns if 'Quantidade Estatística' in col]

# Função para transformar cada grupo de colunas em formato longo
def derreter(df, cols, nome_coluna_valor):
    melted = df.melt(id_vars=id_vars, value_vars=cols,
                     var_name='Ano', value_name=nome_coluna_valor)
    # Extrai apenas o ano como inteiro
    melted['Ano'] = melted['Ano'].str.extract(r'(\d{4})').astype(int)
    return melted

# Transformar cada tipo de dado separadamente
df_valor = derreter(df, valor_cols, 'Valor_FOB_USD')
df_peso = derreter(df, peso_cols, 'Peso_Kg')
df_quant = derreter(df, quant_cols, 'Quantidade')

# Mesclar os três dataframes pelo mesmo conjunto de chaves
df_final = df_valor.merge(df_peso, on=id_vars + ['Ano'])
df_final = df_final.merge(df_quant, on=id_vars + ['Ano'])

# Exibir os primeiros resultados
print(df_final.head())

# Salvar como novo arquivo para usar em dashboards ou análise posterior
df_final.to_csv("./data/dados_exportacao_transformado.csv", index=False)
