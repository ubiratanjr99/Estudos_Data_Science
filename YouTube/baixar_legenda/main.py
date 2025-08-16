from pytubefix import YouTube
import os

url = 'https://www.youtube.com/watch?v=fYxUiG6Q_b8'

yt = YouTube(url)

# Listar as legendas disponíveis
# for i in yt.captions:
#     print(f'Vídeo: {yt.title}')
#     print(f'Código: {i.code} | Idioma: {i.name}')

arquivo = f'legendas/{yt.title}.txt'
legenda = yt.captions['a.pt']

try:
    if legenda:
        transcricao = legenda.generate_srt_captions()
        os.makedirs('legendas', exist_ok=True)

        with open(arquivo, 'w', encoding='utf-8') as escritor:
            escritor.write(transcricao)
        print(f'Legendas do vídeo "{yt.title}" salvas com sucesso!')
    else:
        print(f'Não foram encontradas legendas em PT-BR para o vídeo.')

except Exception as e:
    print(f'Ocorreu um erro: {e}')


