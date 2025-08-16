import requests
import json
import pandas as pd
import os

url = 'https://dogapi.dog/api/v2/facts'

contador = 0
jsonCompleto = []

print('Coletando dados da API...\n')
while contador < 5:
    try:
        response = requests.get(url)
        data = response.json()
        fato = data['data'][0]
        jsonCompleto.append(fato)
        contador += 1
    except requests.exceptions.RequestException as e:
        print(f'Erro ao tentar conexão com a API: {e}')
        break
print('Dados coletados com sucesso.\n')

print('Formatando Json...\n')
df = pd.json_normalize(jsonCompleto)
df.rename(columns={'type': 'Tipo',
          'attributes.body': 'Descrição'}, inplace=True)
print('Json formatado.\n')

print('Montando relatório...\n')
path = 'relatorio.xlsx'
if os.path.exists(path):
    df_existente = pd.read_excel(path)
    novos_dados = df[~df['id'].isin(df_existente['id'])]
    df_concatenado = pd.concat([df_existente, novos_dados], ignore_index=True)
else:
    df_concatenado = df
df_concatenado.to_excel(path, index=False)
print('Relatório finalizado!\n')
