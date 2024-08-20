# Importando as bibliotecas necessarias
import requests
import json
import speech_recognition as sr
import pyttsx3
# pip install speechrecognition
# pip install pyaudio


# Variavel 'reconhecedor' que reconhece sua voz
reconhecedor = sr.Recognizer()
# Iniciando a função da biblioteca pyttsx3 e atribuindo a variável Alexa
alexa = pyttsx3.init()
# Setando a voz volume e palavras por minuto da alexa
alexa.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PT-BR_MARIA_11.0')
alexa.setProperty('volume', 1.0)
alexa.setProperty('rate', '160')

url = "http://localhost:11434/api/generate"

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
        print("O que deseja saber?")
        alexa.say("O que deseja saber?")
        alexa.runAndWait()
        audio = reconhecedor.listen(mic)
        pergunta = reconhecedor.recognize_google(audio, language='pt')

        # pergunta = input("O que deseja saber?")
        alexa.runAndWait()


        print("Aguarde...Carregando...")
        alexa.say("Aguarde...Carregando...")
        alexa.runAndWait()

        input_json = {
            "model": "llama3.1",
            "prompt": "Responda sucintamente em português em poucas palavras em um parágrafo"+pergunta
        }
        response = requests.post(url, json=input_json)
        print(response.text)   #verifique o conteúdo da resposta
        
    linhas = response.text.strip().split('\n')
    valores_response = []

    #processar cada linha como um objeto JSON
    for linha in linhas: 
    #Carregar a linha como um dicionário Python
        obj = json.loads(linha)
    #Obter o valor da chave 'response'
        resposta = obj.get('response')
    #Adicionar a lista de valores de 'response'
        valores_response.append(resposta)
    #juntar os valores de 'reponse' em um única string
    nova_string = ''.join(valores_response)
    #exibir a nova string resultante
    print(nova_string)

    alexa.say(nova_string)
    alexa.runAndWait()
    outra_pergunta()


def outra_pergunta():
    with sr.Microphone() as mic:
        reconhecedor.adjust_for_ambient_noise(mic, duration=2)
        print("Deseja fazer outra pergunta?")
        alexa.say("Deseja fazer outra pergunta?")
        alexa.runAndWait()
        audio = reconhecedor.listen(mic)
        pergunta = reconhecedor.recognize_google(audio, language='pt')
    # pergunta = input("O que deseja saber?")
        if pergunta == "sim":
            alexa.runAndWait()
            print("Ok")
            alexa.say("Ok")
            alexa.runAndWait()
            reconhecedor.adjust_for_ambient_noise(mic, duration=2)
            iniciar_programa()
        elif pergunta == "não":
            alexa.runAndWait()
            print("Ok, Encerrando o programa")
            alexa.say("Ok, Encerrando o programa")
            alexa.runAndWait()
        else:
            alexa.runAndWait()
            print("Desculpe não entendi, iniciando o programa novamente")
            alexa.say("Desculpe não entendi, iniciando o programa novamente")
            alexa.runAndWait()
            iniciar_programa
        
iniciar_programa()
