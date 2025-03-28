import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from elevenlabs import stream
from elevenlabs.client import ElevenLabs
import speech_recognition as sr
import os
import random
import webbrowser
import pywhatkit as kit
import re
from datetime import datetime
import cv2
from openai import OpenAI
import pyaudio
import pvporcupine
import pyaudio
import struct
import pygame  
import cv2
import base64
import variables_gobales
import time
import keyboard
import subprocess
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import psutil
from dotenv import load_dotenv
load_dotenv()
#Proyect root base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FOTOS_DIR = os.path.join(BASE_DIR, 'docs', 'fotos')
AUDIOS_DIR = os.path.join(BASE_DIR, 'docs', 'audios')


def search_online(query):
    # Detectar si el comando es para reproducir en YouTube
    if 'reproduce' in query or 'youtube' in query:
        search_query = query.replace('reproduce ', '').replace('en youtube','').strip()
        kit.playonyt(search_query)
    else:

        # Para búsquedas generales en Google
        search_query = query.replace('busca ', '').replace('google','').strip()
        url = f'https://www.google.com/search?q={search_query}'
        webbrowser.open(url)

def date_and_time(texto):
    hora_y_fecha_actual = datetime.now()

    if 'día' in texto:
        año_actual = hora_y_fecha_actual.strftime("%Y")
        mes_numero = int(hora_y_fecha_actual.strftime("%m"))
        mes_nombre = variables_gobales.months[mes_numero]
        dia_actual = hora_y_fecha_actual.strftime("%d")

        texto_de_fecha = f"Today is {mes_nombre} {dia_actual}, {año_actual}"
        use_voice(texto_de_fecha)
        return 
    elif 'hora' in texto:
        hora_actual_numero = hora_y_fecha_actual.strftime("%I")  # %I para el formato de 12 horas
        minutos_actuales = hora_y_fecha_actual.strftime("%M")
        segundos_actuales = hora_y_fecha_actual.strftime("%S")
        am_pm = hora_y_fecha_actual.strftime("%p")  # AM o PM

        texto_de_hora = f"It is {hora_actual_numero}:{minutos_actuales}:{segundos_actuales} {am_pm}"
        use_voice(texto_de_hora)
        return 

def calculadora(texto):
    numeros_strings = re.findall(r'\d+', texto)
    numeros_ints = [int(num) for num in numeros_strings]  # Convierte los números a enteros
    if 'suma' in texto or 'más' in texto or '+' in texto:
        suma = sum(numeros_ints)  # Suma los números enteros
        use_voice(str(suma)) 
    elif  'resta' in texto or 'menos' in texto or '-' in texto:
        resta = numeros_ints[0] - sum(numeros_ints[1:])
        use_voice(str(resta)) 
    elif 'múltiplica' in texto or 'por' in texto or '*' in texto:
        multiplicacion = 1
        for nums in numeros_ints:
            multiplicacion *= nums

        use_voice(multiplicacion)
    elif 'divide' in texto or 'entre' in texto or 'dividido' in texto or '/' in texto: 
        division = numeros_ints[0]
        for nums in numeros_ints[1:]:
            if nums == 0:
                use_voice('Cant divide that')
    
            division /= nums

        use_voice(division)
        


def tomar_foto(mostrar_preview=True):
    camara = cv2.VideoCapture(0)

    if not camara.isOpened():
        print("No se puede acceder a la cámara")
        return

    ret, frame = camara.read()

    if ret:
        foto_path = os.path.join(FOTOS_DIR, 'foto.jpg')
        cv2.imwrite(foto_path, frame)
        print(f"Foto tomada y guardada en: {foto_path}")
        
        if mostrar_preview:
            cv2.imshow('Vista Previa', frame)
            cv2.waitKey(3000)
            cv2.destroyAllWindows()
        
        frame_con_rostros = detectar_rostros(frame)
        cv2.imwrite(os.path.join(FOTOS_DIR, 'foto_con_rostros.jpg'), frame_con_rostros)

    camara.release()
    cv2.destroyAllWindows()







def detectar_rostros(imagen):
    # Cargar el clasificador de Haar desde la carpeta 'modelos'
    cascada_rostros = cv2.CascadeClassifier('docs/modelos/haarcascade_frontalface_default.xml')

    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Detectar rostros
    rostros = cascada_rostros.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Comprobar si se detectaron rostros y mostrar un mensaje
    if len(rostros) > 0:
        print('Rostros detectados')
    else:
        print("No se detectaron rostros en la imagen.")

    # Dibujar rectángulos alrededor de los rostros detectados
    for (x, y, w, h) in rostros:
        cv2.rectangle(imagen, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return imagen


def is_incomplete_sentence(texto):

    palabras = texto.split()

    # si es incompleta return true
    if palabras[-1] in variables_gobales.palabras_incompletas:
        return True
    return False



def recognice_audio_as_text(audio, recognizer):
    texto = recognizer.recognize_google(audio, language='es')
    texto_en_minuscula = texto.lower()
    return texto_en_minuscula

def get_next_audio_frame(stream, frame_length):
    pcm = stream.read(frame_length, exception_on_overflow=False)
    pcm = struct.unpack_from("h" * frame_length, pcm)
    return pcm

def recognice_word():
    access_key = 'FY82ecHQz/KjhVocJbylShM5Uv6pvoDQtz/6UXIYifUE0lpZMW03uw=='
    porcupine = pvporcupine.create(
        access_key=access_key,
        keywords=['picovoice', 'jarvis']
    )

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=porcupine.sample_rate,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Esperando la frase de activación...")

    try:
        while True:
            audio_frame = get_next_audio_frame(stream, porcupine.frame_length)
            keyword_index = porcupine.process(audio_frame)

            if keyword_index == 0:
                return True
            elif keyword_index == 1:
                return True
                

    except KeyboardInterrupt:
        print("Detenido por el usuario")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

##use voice
def use_voice(phrase): 
    import os
    from elevenlabs import stream
    from elevenlabs.client import ElevenLabs

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("API key de ElevenLabs not found. See .env file")

    client = ElevenLabs(api_key=api_key)

    audio_stream = client.text_to_speech.convert_as_stream(
        text=phrase,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_flash_v2_5"
    )

    stream(audio_stream)



def create_file(file_name, content): 
    with open(file_name,'w') as file: 
        file.write(content)


def play_audio(subfolder, aleatorio=True, contexto=""):
    folder = os.path.join(AUDIOS_DIR, subfolder)
    archivos_validos = [f for f in os.listdir(folder) if f.endswith((".wav", ".mp3", ".ogg"))]

    if not archivos_validos:
        print("No hay archivos de audio en la carpeta seleccionada.")
        return

    if aleatorio:
        selected_file = random.choice(archivos_validos)
    else:
        contexto_map = {
            'no_entender': 0,
            'foto': 1,
            'bye': 2,
            'no_especifico_buscar': 3,
            'preguntar mensaje': 4,
            'mensaje enviado': 5,
            'no esta en contactos': 6
        }
        index = contexto_map.get(contexto)
        if index is None or index >= len(archivos_validos):
            print(f"Contexto '{contexto}' no válido.")
            return
        selected_file = archivos_validos[index]

    path = os.path.join(folder, selected_file)

    if os.path.exists(path):
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue


def enviar_whatsapp(persona):
    if persona not in variables_gobales.contactos: 
        play_audio("otros",contexto="no esta en contactos",aleatorio=False)
        return 
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Ajustar para el ruido ambiental
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 1.9
        play_audio("otros",contexto="preguntar mensaje",aleatorio=False)
        audio = recognizer.listen(source, phrase_time_limit=None)
        mensaje = recognice_audio_as_text(audio, recognizer)
    kit.sendwhatmsg_instantly(variables_gobales.contactos[persona], mensaje,15, close_time= 3, tab_close=True) 
    play_audio("otros",contexto="mensaje enviado",aleatorio=False)



client = OpenAI()
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def chatgpt(audio,search=False, imagen = False):

    if search == True: 
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": '''
                    Vas a decir la palabra o frase que te indique dependiendo del contexto. Solo di la palabra o frase, nada mas (todo lo que digas dilo en minuscula). 
                    Case_1:quiere cerrar spotify, di 'cierra spotify'
                    Case_2:quiere cerrar el buscador, di 'cierra edge'
                    Case_3:buscar algo en el buscador, di 'busca {y aqui pones lo que sea que quiere buscar la persona}'
                    Case_4:saber la hora, di 'qué hora es'
                    Case_5:saber qué día es, di 'qué día es'
                    Case_6:tomar una foto, di 'toma foto' 
                    Case_7:reproducir un video especificamente en youtube: di 'reproduce {y aqui pones lo que sea quie quiere reproducir la persona}'
                    Case_8:crear un archivo, di 'crearArchivo {aqui el nombre del archivo con el formato que te dijeron} {y aqui pones todo lo que la persona te pidio que pusieras, con todo y el espaciado corregido}'
                    Case_9:apagarte o parar, di 'stop'
                    Case_10: si quiere enviarle un mensaje a alguien, di 'whatsapp {y aqui el nombre de la persona}' '
                    Case_11:quiere que mires u observes algo y lo analices (ten en cuenta que el programa va a tomar una foto de lo que quiere que mires), di 'analizalaimagen {y aqui lo exactamente lo que la persona dijo no omitas  ni resumas informacion}'
                    Case_12: quiere cerrar una pestaña del buscador, di 'cierra pestaña'
                    Case_13: quiere hablar con copilot, di 'abre copilot'
                    Case_14: quiere abrir o ver netflix, di 'abre netflix'
                    Case_15: quiere cerrar el programa o netflix, di 'cierra app'
                    Case_16: poner, bajar o subir el volumen, di 'establecervolumen {y aquí el número (solo el número, sin el simbolo de %)}'
                    Case_17: poner una canción, di 'spotify {y aquí pones el nombre y/o datos de la canción}'
                    Case_18: quiere continuar/parar espeficifamente musica o spotify, di 'para musica'
                    Case_19: quiere pausar/continuar algo (y no es musica), di 'pausa video'
                    Case_20: quiere saber algo, di: 'jarvis {y aqui lo que sea que la persona dijo(no omitas informacion)}'
                    '''},
                    {"role": "user", "content": audio}
                    ],
            response_format={
                "type": "text"
                },
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )    
    elif imagen == True:
        tomar_foto()
        play_audio("frases")
        image_path = r"C:\\Users\\antof\\OneDrive\\Documents\\python class\\proyectos\\asistente\\docs\\fotos\\foto.jpg"
        base64_image = encode_image(image_path)
        if not isinstance(base64_image, str):
            print("Error: La imagen codificada no es una cadena de texto.")
        else:
            response = client.chat.completions.create(
            model="gpt-4o-mini",  # Asegúrate de usar un modelo que soporte imágenes
            messages=[
                {"role": "user", 
                "content": [
                    {"type": "text", "text": audio},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ],
            max_tokens=300,
            )
        print('se analizo la imagen che ')
        use_voice(response.choices[0].message.content)
        

    return response.choices[0].message.content



# Almacenar el historial de la conversación

def conversation_with_assistant(text):

    # Inicializar el historial de conversación con la instrucción de sistema.
    conversation_history = [
        {"role": "system", "content": "Eres un muy buen asistente."}
    ]
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Ajustar para el ruido ambiental
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 1.9
        
        #add the argumento to the converdsation history 
        conversation_history.append({"role": "user", "content": text})
        response = client.chat.completions.create(
                model="gpt-3.5-turbo",  
                messages=conversation_history
            )
        assistant_response = response.choices[0].message.content
        use_voice(assistant_response)
        while True:
            audio_data = recognizer.listen(source, phrase_time_limit=None)
            user_text = recognice_audio_as_text(audio_data, recognizer)
            if user_text is None:
                error_msg = "No se pudo reconocer el audio, intenta nuevamente."
                print(error_msg)
                continue
            # Salir de la conversación si el usuario dice "salir"
            texto_dividido = user_text.lower()
            texto_minuscula = texto_dividido.split()
            if ('para'or 'detente') in texto_minuscula:
                break

            # Agregar el mensaje del usuario al historial
            conversation_history.append({"role": "user", "content": user_text})
            
            # Llamada a la API de OpenAI con el historial de la conversación
            response = client.chat.completions.create(
                model="gpt-4o-mini",  
                messages=conversation_history
            )

            # Extraer la respuesta del asistente
            assistant_response = response.choices[0].message.content
            conversation_history.append({"role": "assistant", "content": assistant_response})
            
            use_voice(assistant_response)

def abrir_copilot(): 

    subprocess.Popen(["start", "msedge"], shell=True)
    time.sleep(3)

    keyboard.press_and_release('ctrl+shift+.')
    time.sleep(1)  # Pausa breve entre cada Tab por seguridad

    keyboard.press_and_release('tab')
    time.sleep(0.2)

    keyboard.press_and_release('enter')

def abrir_netflix():
    keyboard.press_and_release('win')
    time.sleep(1) 

    keyboard.write('netflix')
    time.sleep(1)  

    keyboard.press_and_release('enter')
    time.sleep(5)  

    keyboard.press_and_release('f11')

def bajar_volumen_a_cero():
    #obtener dispositivo de audio 
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    
    # Obtener el volumen actual
    volumen_actual = volume.GetMasterVolumeLevelScalar()  # Escalar (0.0 a 1.0)
    play_audio("preguntas")
    # Bajar el volumen a 0%
    volume.SetMasterVolumeLevelScalar(0.0, None)
    
    # Retornar el volumen original
    return volumen_actual

def restaurar_volumen(volumen_original):
    # Obtener el dispositivo de audio
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    
    # Restaurar el volumen al nivel original
    volume.SetMasterVolumeLevelScalar(volumen_original, None)

def establecer_volumen(nivel):
    if nivel < 0 or nivel > 100:
        return
    
    # Convertir el nivel de pFseorcentaje a un escalar (0.0 a 1.0)
    nivel_escalar = nivel / 100.0

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    # Establecer el volumen al nivel deseado
    volume.SetMasterVolumeLevelScalar(nivel_escalar, None)
    print(f"Volumen establecido en {nivel}%")

#verifica si ya esta en ejecucion 
def verificar_spotify_abierto():
    # Iterar sobre todos los procesos en ejecución
    for proceso in psutil.process_iter(['name']):
        try:
            # Verificar si el nombre del proceso es "Spotify.exe"
            if proceso.info['name'] and 'Spotify' in proceso.info['name']:
                #si esta abierto returnea True
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    #false si esta cerrado
    return False

# def buscar_cancion_spotify(cancion): 
#     entrar_spotify()
#     #verifica si el proceso ya estaba antes en ejecucion 
#     if verificar_spotify_abierto(): 
#         time.sleep(0.5)
#     else: 
#         time.sleep(7)
#     keyboard.press_and_release('ctrl+k')
#     time.sleep(0.5)
#     keyboard.press_and_release('ctrl+a')
#     time.sleep(0.5)
#     keyboard.press_and_release('ctrl+delete')
#     time.sleep(1)
#     keyboard.write(cancion)
#     time.sleep(5)
#     keyboard.press_and_release('shift+enter')
#     time.sleep(1)
#     keyboard.press_and_release('enter')
#     time.sleep(1)


def detener_reproduccion(): 
    if verificar_spotify_abierto():
        entrar_spotify()
        time.sleep(1)
        keyboard.press_and_release('spacebar')
        time.sleep(1)

#pausar o continuar video: 
def pausar_continuar_video(): 
    keyboard.press_and_release('k')
    time.sleep(1)
#escribe spotify y enter en la barra de comandos 
def entrar_spotify(): 
    keyboard.press_and_release('win+s')
    time.sleep(1)
    keyboard.write('spotify')
    time.sleep(1)
    keyboard.press_and_release('enter')