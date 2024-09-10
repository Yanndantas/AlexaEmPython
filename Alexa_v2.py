# Importando as bibliotecas necessárias
import requests
import json 
import speech_recognition as sr
import pyttsx3
import os
import datetime
import subprocess
import pyautogui
import time
import base64   
import webbrowser
import random


#Site da API para iniciar a função clima clima
#https://openweathermap.org/current

#Site da API do spotify

# Variável 'reconhecedor' que reconhece sua voz
reconhecedor = sr.Recognizer()
# Iniciando a função da biblioteca pyttsx3 e atribuindo a variável alexa
alexa = pyttsx3.init()
# Setando a voz, volume e palavras por minuto da alexa
alexa.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PT-BR_MARIA_11.0')
alexa.setProperty('volume', 1.0)
alexa.setProperty('rate', '160')

url = "http://localhost:11434/api/generate"

horas_faladas = []
minutos_falados = []


# Função de ativação quando falamos "alexa" utilizando de um loop while que persiste até
# o programa entender o "alexa" alexa
def ouvir_comando_inicial():
    with sr.Microphone() as mic:
        reconhecedor.adjust_for_ambient_noise(mic, duration=2)
        print('Aguardando o comando')
        while True:
            audio = reconhecedor.listen(mic)
            try:
                comando = reconhecedor.recognize_google(audio, language='pt').lower()
                if "alexa" in comando:
                    print("Comando detectado: 'alexa'")
                    iniciar_programa()
                    break
            except sr.UnknownValueError:
                print("Não entendi o que foi dito, tentando novamente...")
            except sr.RequestError as e:
                print(f"Erro ao se comunicar com o serviço de reconhecimento de fala: {e}")

def terminate():
    print("Ok encerrando o programa")
    alexa.say("Ok encerrando o programa")
    alexa.runAndWait()
    os.system('cls')
    # sys.exit()


def iniciar_programa():
    print('''

░█████╗░██╗░░░░░███████╗██╗░░██╗░█████╗░
██╔══██╗██║░░░░░██╔════╝╚██╗██╔╝██╔══██╗
███████║██║░░░░░█████╗░░░╚███╔╝░███████║
██╔══██║██║░░░░░██╔══╝░░░██╔██╗░██╔══██║
██║░░██║███████╗███████╗██╔╝╚██╗██║░░██║
╚═╝░░╚═╝╚══════╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
            ''')
    with sr.Microphone() as mic:
        reconhecedor.adjust_for_ambient_noise(mic, duration=2)
        print("Com o que posso ajudar?")
        alexa.say("Com o que posso ajudar?")
        alexa.runAndWait()
        audio = reconhecedor.listen(mic)
        pergunta = reconhecedor.recognize_google(audio, language='pt').strip().lower()
#Separando as formas de ativar as funções
        Funcoes = {
    "que horas são": falar_as_horas,
    "alexa que horas são": falar_as_horas,
    "me diga as horas": falar_as_horas,

    "cadastrar evento na agenda": cadastrar_evento,
    "cadastrar evento": cadastrar_evento,
    "cadastre um evento": cadastrar_evento,
    "ler agenda": ler_eventos,

    "leia minha agenda": ler_eventos,
    "leia a minha agenda": ler_eventos,
    "leia meus eventos": ler_eventos,
    "leia minha agenda": ler_eventos,

    "clima": clima,
    "como esta o clima": clima,  
    "alexa como está o clima": clima,  

    "toque uma musica": tocar_musica_spotify,
    "abrir spotify": tocar_musica_spotify,
    "abra o spotify": tocar_musica_spotify,
    "abre o spotify": tocar_musica_spotify,
    "abre o spotify": tocar_musica_spotify,
    "toque uma musica": tocar_musica_spotify,
    "tocar musica": tocar_musica_spotify,

    "jogar forca": jogar_forca,
    "abra o jogo da forca": jogar_forca,
    "abrir jogo da forca": jogar_forca,

    "jogar adivinhação":jogar_adivinhacao,
    "jogo da adivinhação":jogar_adivinhacao,

    "encerrar programa": terminate,
    "encerrar": terminate,
    "sair": terminate,
    "não": terminate
}

        acao = Funcoes.get(pergunta)
        if acao:
            acao()
        else:
            alexa.runAndWait()
            print("Aguarde...Carregando...")
            alexa.say("Aguarde...Carregando...")
            alexa.runAndWait()

            input_json = {
                "model": "llama3.1",
                "prompt": "Responda sucintamente em português em poucas palavras em um parágrafo: " + pergunta
            }
            response = requests.post(url, json=input_json)
            print(response.text)  # Verifique o conteúdo da resposta

            linhas = response.text.strip().split('\n')
            valores_response = []
            for linha in linhas:
                obj = json.loads(linha)
                resposta = obj.get('response')
                valores_response.append(resposta)

            nova_string = ''.join(valores_response)
            print(nova_string)

            alexa.say(nova_string)
            alexa.runAndWait()
            outra_pergunta()


# Utilizando da API do spotify for developers eu consegui utilizar desta forma, antes eu estava fazendo
# Com controlador de interface com a biblioteca pyautogui mas consegui utilizar o controle diretamente pela API


# Define a função para obter o token de reconhecimento para poder utilizar a API
def obter_token_spotify(client_id, client_secret):
    client_id = '7755d17286954e46a3a1caf89709ef1f'
    client_secret = 'f826a3f5d618412ba9db80c9b75a5bfd'
    url_API_spotify = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url_API_spotify, headers=headers, data=data)
    response_data = response.json()
    return response_data.get('access_token')
# Define a função ja utilizando a API para encontrar as musicas
def buscar_musica(token, query):
    url_busca = f'https://api.spotify.com/v1/search?q={query}&type=track&limit=1'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url_busca, headers=headers)
    response_data = response.json()
    tracks = response_data.get('tracks', {}).get('items', [])
    if tracks:
        return tracks[0].get('uri')
    return None
def tocar_musica_spotify():
    client_id = '7755d17286954e46a3a1caf89709ef1f'
    client_secret = 'f826a3f5d618412ba9db80c9b75a5bfd'
    token_acesso = obter_token_spotify(client_id, client_secret)
    
    if not token_acesso:
        alexa.say("Não consegui obter um token de acesso do Spotify.")
        alexa.runAndWait()
        return
    
    with sr.Microphone() as mic:
        reconhecedor.adjust_for_ambient_noise(mic, duration=2)
        alexa.say("Qual música você gostaria de tocar?")
        alexa.runAndWait()
        
        audio = reconhecedor.listen(mic)
        musica = reconhecedor.recognize_google(audio, language='pt').strip()
        
        alexa.say(f"Tocando {musica} no Spotify.")
        alexa.runAndWait()
        
        musica_uri = buscar_musica(token_acesso, musica)
        
        if musica_uri:
            webbrowser.open(f'spotify:/{musica_uri}')
            alexa.say("A música deve estar tocando agora.")
            alexa.runAndWait()
        else:
            alexa.say("Não consegui encontrar a música.")
            alexa.runAndWait()


def jogar_forca():
    palavras = ["programacao"]
    palavra = random.choice(palavras)
    letras_adivinhadas = set()
    tentativas = 6

    while tentativas > 0:
        palavra_oculta = ''.join([letra if letra in letras_adivinhadas else '_' for letra in palavra])
        print("Palavra:", palavra_oculta)
        print(f"Tentativas restantes: {tentativas}")

        palpite = input("Adivinhe uma letra: ").lower()
        if palpite in letras_adivinhadas:
            print("Você já tentou essa letra.")
        elif palpite in palavra:
            letras_adivinhadas.add(palpite)
            if set(palavra) == letras_adivinhadas:
                print("Parabéns! Você adivinhou a palavra:", palavra)
                break
        else:
            tentativas -= 1
            print("Letra incorreta.")

    if tentativas == 0:
        print("Você perdeu. A palavra era:", palavra)

def jogar_adivinhacao():
    numero_secreto = random.randint(1, 100)
    tentativas = 0

    alexa.say("Vamos jogar adivinhação. Tente adivinhar um número entre 1 e 100.")
    alexa.runAndWait()

    while True:
        try:
            with sr.Microphone() as mic:
                reconhecedor.adjust_for_ambient_noise(mic, duration=2)
                alexa.say("Qual é o seu palpite?")
                alexa.runAndWait()

                audio = reconhecedor.listen(mic)
                palpite = reconhecedor.recognize_google(audio, language='pt').strip().lower()

                if palpite.isdigit():
                    palpite = int(palpite)
                    tentativas += 1

                    if palpite < numero_secreto:
                        alexa.say("O número secreto é maior.")
                        alexa.runAndWait()
                    elif palpite > numero_secreto:
                        alexa.say("O número secreto é menor.")
                        alexa.runAndWait()
                    else:
                        print(f"Parabéns! Você acertou o número em {tentativas} tentativas.")
                        alexa.say(f"Parabéns! Você acertou o número em {tentativas} tentativas.")
                        alexa.runAndWait()
                        break
                else:
                    alexa.say("Por favor, insira um número válido.")
                    alexa.runAndWait()
        except sr.UnknownValueError:
            alexa.say("Não consegui entender, por favor, tente novamente.")
            alexa.runAndWait()
        except ValueError:
            alexa.say("Por favor, insira um número válido.")
            alexa.runAndWait()


def clima():
    # Definindo minha chave da API do site openweathermap
    chave_api = 'edd780a23027b9491bfba602dbbdeed2'
    cidade = 'São Paulo'
    
    # URL da API para obter as coordenadas de São Paulo
    url_loc = f'http://api.openweathermap.org/geo/1.0/direct?q={cidade}&limit=1&appid={chave_api}'

    try:
        # Fazendo a requisição para obter as coordenadas
        resposta_loc = requests.get(url_loc)
        dados_loc = resposta_loc.json()
        
        # Verificar se a resposta contém dados
        if resposta_loc.status_code == 200 and dados_loc:
            lat = dados_loc[0]['lat']
            lon = dados_loc[0]['lon']
            
            # URL da API para obter o clima usando as coordenadas
            url_clima = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={chave_api}&lang=pt_br&units=metric'

            # Fazendo a requisição para obter o clima
            resposta_clima = requests.get(url_clima)
            dados_clima = resposta_clima.json()

            # Verificar o conteúdo da resposta do clima
            if resposta_clima.status_code == 200:
                temp_atual = dados_clima['main']['temp']
                descricao = dados_clima['weather'][0]['description']
                resposta_clima_texto = f"A temperatura atual em {cidade} é de {temp_atual}°C com {descricao}."
            else:
                resposta_clima_texto = "Desculpe, não consegui obter o clima agora."
        else:
            resposta_clima_texto = "Desculpe, não consegui encontrar a localização de São Paulo."

    except Exception as e:
        resposta_clima_texto = f"Ocorreu um erro ao obter o clima: {e}"
        print(f"Erro detalhado: {e}")
    
    print(resposta_clima_texto)
    alexa.say(resposta_clima_texto)
    alexa.runAndWait()
    outra_pergunta()


def falar_as_horas():
    agora = datetime.datetime.now()
    horas = agora.strftime('%H')
    minutos = agora.strftime('%M')

# Tratamento para a alexa não falar "zero" quando tiver um zero nas horas por exemplo "oito horas e zero nove minutos"
    if horas.startswith('0'):
        horas_faladas = horas[1]
    else:
        horas_faladas = horas

    if minutos.startswith('0'):
        minutos_falados = minutos[1]  # Fala apenas o segundo dígito dos minutos
    else:
        minutos_falados = minutos

    print(f'Agora são {horas_faladas} horas e {minutos_falados} minutos.')
    alexa.say(f'Agora são {horas_faladas} horas e {minutos_falados} minutos.')
    alexa.runAndWait()
    outra_pergunta()


def cadastrar_evento():
    with sr.Microphone() as mic:
        reconhecedor.adjust_for_ambient_noise(mic, duration=2)
        print("Ok, qual evento devo cadastrar?")
        alexa.say("Ok, qual evento devo cadastrar?")
        alexa.runAndWait()
        audio = reconhecedor.listen(mic)
        evento = reconhecedor.recognize_google(audio, language='pt').strip()

        if evento:
            arquivo = 'eventos.txt'
            with open(arquivo, 'a', encoding='utf-8') as f:
                f.write(f"{evento}\n")
            
            print("Evento cadastrado com sucesso.")
            alexa.say("Evento cadastrado com sucesso")
        else:
            print("Desculpe, não entendi o evento.")
            alexa.say("Desculpe, não entendi o evento.")
        
        alexa.runAndWait()
        outra_pergunta()


def ler_eventos():
    arquivo = 'eventos.txt'
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            eventos = f.read().strip()
            if eventos:
                print("Lendo eventos...")
                alexa.say("Aqui estão os eventos cadastrados:")
                alexa.say(eventos)
            else:
                print("Não há eventos cadastrados.")
                alexa.say("Não há eventos cadastrados.")
    else:
        print("O arquivo de eventos não existe.")
        alexa.say("O arquivo de eventos não existe.")
    
    alexa.runAndWait()
    outra_pergunta()


# Um simples loop para saber se o usuário deseja algo mais
def outra_pergunta():
    with sr.Microphone() as mic:
        reconhecedor.adjust_for_ambient_noise(mic, duration=2)
        print("Deseja mais alguma coisa?")
        alexa.say("Deseja mais alguma coisa?")
        alexa.runAndWait()
        audio = reconhecedor.listen(mic)
        pergunta = reconhecedor.recognize_google(audio, language='pt').strip().lower()
        

        Funcoes = {
    "que horas são": falar_as_horas,
    "alexa que horas são": falar_as_horas,
    "alexa me diga as horas": falar_as_horas,
    "me diga as horas": falar_as_horas,

    "cadastrar evento na agenda": cadastrar_evento,
    "cadastrar evento": cadastrar_evento,
    "alexa cadastre um evento": cadastrar_evento,
    "ler agenda": ler_eventos,

    "leia minha agenda": ler_eventos,
    "alexa leia a minha agenda": ler_eventos,
    "leia meus eventos": ler_eventos,
    "alexa leia minha agenda": ler_eventos,

    "como esta o clima": clima,  # Novo comando adicionado
    "alexa como está o clima": clima,  # Novo comando adicionado

    "toque uma musica": tocar_musica_spotify,
    "abrir spotify": tocar_musica_spotify,
    "alexa abra o spotify": tocar_musica_spotify,
    "alexa abre o spotify": tocar_musica_spotify,
    "abre o spotify": tocar_musica_spotify,
    "alexa toque uma musica": tocar_musica_spotify,
    "tocar musica": tocar_musica_spotify,



    "encerrar programa": terminate,
    "encerrar": terminate,
    "sair": terminate,
    "não": terminate
}
        acao = Funcoes.get(pergunta)
        if acao:
            acao()
        elif alexa.runAndWait():
            print("Aguarde...Carregando...")
            alexa.say("Aguarde...Carregando...")
            alexa.runAndWait()

            input_json = {
                "model": "llama3.1",
                "prompt": "Responda sucintamente em português em poucas palavras em um parágrafo: " + pergunta
            }
            response = requests.post(url, json=input_json)
            print(response.text)  # Verifique o conteúdo da resposta

            linhas = response.text.strip().split('\n')
            valores_response = []
            for linha in linhas:
                obj = json.loads(linha)
                resposta = obj.get('response')
                valores_response.append(resposta)

            nova_string = ''.join(valores_response)
            print(nova_string)

            alexa.say(nova_string)
            alexa.runAndWait()
        else:
            outra_pergunta()

        # # Executa a função correspondente à pergunta ou uma ação padrão
        # acao = Funcoes.get(pergunta, lambda: alexa.say("Comando não reconhecido."))
        # acao()
        # alexa.runAndWait()


        # iniciar_programa()


# Inicia o programa com a função que foi definida no inicio do código
ouvir_comando_inicial()
