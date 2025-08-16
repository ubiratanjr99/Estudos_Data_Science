import requests
import json
import pandas as pd
import os

qtd_users = 200
format = 'json'
url = f'https://randomuser.me/api/?results={qtd_users}&format={format}'

response = requests.get(url)
dados = response.json()

print('\nColetando os dados da API...\n')
df = pd.json_normalize(dados['results'])

df.drop(columns=[
       'location.coordinates.latitude',
       'location.coordinates.longitude', 
       'location.timezone.offset',
       'location.timezone.description', 
       'login.uuid', 
       'login.salt', 
       'login.md5', 
       'login.sha1',
       'login.sha256', 
       'dob.date', 
       'registered.age', 
       'registered.date',
       'id.name', 
       'id.value'
       ], 
       inplace=True)

df.rename(columns={'gender': 'Gênero',
                   'phone': 'Telefone',
                   'cell': 'Celular',
                   'nat': 'Naturalidade',
                   'name.title': 'Prefixo',
                   'name.first': 'Primeiro_Nome', 
                   'name.last': 'Último_Nome', 
                   'location.street.number': 'N°',
                   'location.street.name': 'Rua',
                   'location.city': 'Cidade',
                   'location.state': 'Estado',
                   'location.country': 'País',
                   'location.postcode': 'Cod_Postal',
                   'login.username': 'Username',
                   'login.password': 'Senha',
                   'dob.age': 'Idade',
                   'picture.large': 'Foto_Grande',
                   'picture.medium': 'Foto_Média',
                   'picture.thumbnail': 'Thumbnail'
                   },
                   inplace=True)

path = 'relatorio.xlsx'

print('Montando relatório...\n')
if os.path.exists(path):
    df_existente = pd.read_excel(path)
    novos_dados = df[~df['Username'].isin(df_existente['Username'])]
    df_final = pd.concat([df_existente, novos_dados], ignore_index=True)
else:
    df_final = df
df_final.to_excel(path, index=False)

total_usuarios = len(df_final)

print('Dados exportados e relatório concluído!\n\n'+
      f'Quantidade de novos usuários: {qtd_users}\n'+
      f'Quantidade total de usuários no relatório: {total_usuarios}\n')