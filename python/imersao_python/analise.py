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



# Aula 3 - Manipulação de dados


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


maior = df_principal['variacao_rs'].max()
menor = df_principal['variacao_rs'].min()
media = df_principal['variacao_rs'].mean()
media_lucro = df_principal[df_principal['Resultado'] == 'Lucro']['variacao_rs'].mean()
media_preju = df_principal[df_principal['Resultado'] == 'Prejuízo']['variacao_rs'].mean()
print(f"Maior\tR$ {maior:,.2f}")
print(f"Menor\tR$ {menor:,.2f}")
print(f"Média\tR$ {media:,.2f}")
print(f"Média lucro\tR$ {media_lucro:,.2f}")
print(f"Média Prejuízo\tR$ {media_preju:,.2f}")


df_principal_lucro = df_principal[df_principal['Resultado'] == 'Lucro']
df_principal_lucro


df_analise_segmento = df_principal_lucro.groupby('Segmento')['variacao_rs'].sum().reset_index()
df_analise_segmento


df_analise_saldo = df_principal.groupby('Resultado')['variacao_rs'].sum().reset_index()
df_analise_saldo


fig = px.bar(df_analise_saldo, x = 'Resultado', y = 'variacao_rs', text = 'variacao_rs', title = 'Variação em reais por resultado')
fig.show()


fig = px.bar(df_analise_segmento, x = 'Segmento', y = 'variacao_rs', text = 'variacao_rs', title = 'Variação em reais por segmento')
fig.show()


fig = px.pie(df_analise_segmento, names='Segmento', values='variacao_rs', title='Variação Reais por Segmento')
fig.show()


df_analise_cat_idade = df_principal.groupby('Cat_idade')['variacao_rs'].sum().reset_index()
df_analise_cat_idade
fig = px.bar(df_analise_cat_idade, x='Cat_idade', y='variacao_rs', text='variacao_rs', title='Variação Reais por Categoria de Idade')
fig.show()


# Aula 4 - Análises avançadas e gráficos de vela

!pip install mplfinance

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots


dados = yf.download('PETR4.SA', start = '2023-01-01', end = '2023-12-31')
dados


dados.columns = ['Abertura', 'Maximo', 'Minimo', 'Fechamento', 'Fech_Ajust', 'Volume']
dados = dados.rename_axis('Data')
dados


dados['Fechamento'].plot(figsize=(10, 6))
plt.title('Variação do preço por data', fontsize = 16)
plt.legend(['Fechamento'])


df = dados.head(60).copy()
df['Data'] = df.index
df['Data'] = df['Data'].apply(mdates.date2num)
df


fig, ax = plt.subplots(figsize = (15, 8))
width = 0.7
for i in range(len(df)):
  if df['Fechamento'].iloc[i] > df['Abertura'].iloc[i]:
    color = 'green'
  else:
    color = 'red'

ax.plot([df['Data'].iloc[i], df['Data'].iloc[i]]
        [df['Minimo'].iloc[i], df['Maximo'].iloc[i]],
        color = color
        linewidth = 1)

ax.add_patch(plt.Rectangle((df['Data'].iloc[i] - width / 2, min(df['Abertura'].iloc[i], df['Fechamento'].iloc[i])),
                           width,
                           abs(df['Fechamento'].iloc[i] - df['Abertura'].iloc[i]),
                           facecolor = color))

# ----------- FIM GRÁFICO Candlestick ----------- #
# ----------- INÍCIO GRÁFICO Volume e Candlestick ----------- #

fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.1,
                    subplot_titles=('Candlesticks', 'Volume Transacionado'),
                    row_width=[0.2, 0.7])

# Adicionando gráfico de candlestick
fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Abertura'],
                             high=df['Maximo'],
                             low=df['Minimo'],
                             close=df['Fechamento'],
                             name='Candlestick'),
               row=1, col=1)

# Adicionando médias móveis ao mesmo subplot para análise de tendências
fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA7'],
                         mode='lines',
                         name='MA7 - Média Móvel 7 Dias'),
               row=1, col=1)

# Transformando o gráfico de scatter em um gráfico de barras verticais com cor roxa
fig.add_trace(go.Bar(x=df.index,
                     y=df['Volume'],
                     name='Volume',
                     marker_color='blue'),  # Definindo a cor roxa
               row=2, col=1)

# Atualizando layout
fig.update_layout(yaxis_title='Preço',
                  xaxis_rangeslider_visible=False,
                  width=1100, height=600)

# Mostrando gráfico
fig.show()

# ----------- FIM GRÁFICO Volume e Candlestick ----------- #

dados = yf.download('PETR4.SA', start = '2023-01-01', end = '2023-12-31')


mpf.plot(dados.head(60), type = 'candle', figsize = (16, 8), volume = True, mav = (7, 14), style='brasil')


# desafio aula 4

apple_data = yf.download('AAPL', start = '2023-01-01', end = '2023-12-31')
mpf.plot((apple_data.head(60)), type='candle', figsize = (18,10), volume=True, mav=(7,14), style='yahoo')


# Aula 5 - Machine learning e séries temporais de ações

from prophet import Prophet

dados = yf.download('MSFT', start = '2020-01-01', end = '2023-12-31', progress = False)
dados = dados.reset_index()
dados

dados_prophet_treino = dados[['Date', 'Close']].rename(columns = {'Date':'ds', 'Close':'y'})

# Criar e treinar o modelo
modelo = Prophet(weekly_seasonality = True,
                 yearly_seasonality = True,
                 daily_seasonality = False)

modelo.add_country_holidays(country_name = 'US')

modelo.fit(dados_prophet_treino)


# Criar datas futuras para previsão até o final de 2023
futuro = modelo.make_future_dataframe(periods = 150)
previsao = modelo.predict(futuro)


# Plotar os dados de treino, teste e previsões
plt.figure(figsize = (14, 8))
plt.plot(dados_treino['Date'], dados_treino['Close'], label = 'Dados de treino', color = 'blue')
plt.plot(dados_teste['Date'], dados_teste['Close'], label = 'Dados reais (Teste)', color = 'green')
plt.plot(previsao['ds'], previsao['yhat'], label = 'Previsão', color = 'orange', linestyle = '--')

plt.axvline(dados_treino['Date'].max(), color = 'red', linestyle = '--', label = 'Início da previsão')
plt.xlabel('Data')
plt.ylabel('Preço de fechamento')
plt.title('Previsão de preço de fechamento vs dados reais')
plt.legend()
plt.show()