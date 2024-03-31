#! python

# Aula 2 - Importação
import pandas as pd


df_principal = pd.read_excel('/content/Imersão Python - Tabela de ações.xlsx', sheet_name='Principal')
df_principal


df_total_acoes = pd.read_excel('/content/Imersão Python - Tabela de ações.xlsx', sheet_name='Total_de_acoes')
df_total_acoes


df_ticker = pd.read_excel('/content/Imersão Python - Tabela de ações.xlsx', sheet_name='Ticker')
df_ticker


df_chatgpt = pd.read_excel('/content/Imersão Python - Tabela de ações.xlsx', sheet_name='Planilha4')
df_chatgpt


'''
 Aula 3 - Manipulação de dados
'''

df_principal = df_principal[['Ativo', 'Data', 'Último (R$)', 'Var. Dia (%)']].copy()
df_principal


df_principal = df_principal.rename(columns={'Último (R$)':'ultimo_valor', 'Var. Dia (%)':'var_dia_pct'}).copy()
df_principal


df_principal['var_pct'] = df_principal['var_dia_pct'] / 100
df_principal['valor_incial'] = df_principal['var_dia_pct'] / (df_principal['var_pct'] + 1)
df_principal


df_principal = df_principal.merge(df_total_acoes, left_on = 'Ativo', right_on = 'Código', how = 'left')
df_principal


df_principal = df_principal.drop(columns=['Código'])
df_principal


df_principal['variacao_rs'] = (df_principal['ultimo_valor'] - df_principal['valor_incial']) * df_principal['Qtde. Teórica']
df_principal


pd.options.display.float_format = '{:.2f}'.format
df_principal['Qtde. Teórica'] = df_principal['Qtde. Teórica'].astype(int)
df_principal


df_principal = df_principal.rename(columns={'Qtde. Teórica':'qtde_teorica'}).copy()
df_principal


df_principal['Resultado'] = df_principal['variacao_rs'].apply(lambda x: 'Lucro' if x > 0 else ('Prejuízo'))
df_principal


df_principal = df_principal.merge(df_ticker, left_on = 'Ativo', right_on = 'Ticker', how = 'left')
df_principal = df_principal.drop(columns = ['Ticker'])
df_principal


df_principal = df_principal.merge(df_chatgpt, left_on = 'Nome', right_on = 'Nome da empresa', how = 'left')
df_principal = df_principal.drop(columns = ['Nome da empresa'])
df_principal


df_principal['Cat_idade'] = df_principal['Idade'].apply(lambda x: 'Mais de 100 anos' if x > 100 else ('Entre 50 e 100 anos'))
df_principal