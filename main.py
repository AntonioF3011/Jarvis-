import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from funciones import recognice_audio_as_text,recognice_word,is_incomplete_sentence, search_online, establecer_volumen, pausar_continuar_video
import speech_recognition as sr
from funciones import play_audio, date_and_time, tomar_foto, chatgpt, conversation_with_assistant, enviar_whatsapp, abrir_copilot, abrir_netflix, bajar_volumen_a_cero, restaurar_volumen, detener_reproduccion
import keyboard


if __name__ == "__main__":
    recognizer = sr.Recognizer()
    mic = sr.Microphone()  
    stop = True
    music_playing = False  # if spotify is reproducing music then True

    while stop:
        if recognice_word():  # Palabra clave reconocida
            with mic as source:
                # Ajustar ruido ambiental en cada iteración para adaptarse al entorno
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                recognizer.pause_threshold = 1.9  # Configuración del tiempo de pausa
                volumen_actual = bajar_volumen_a_cero()
                audio = recognizer.listen(source, phrase_time_limit=None)
                restaurar_volumen(volumen_actual)
            # Transcribe el audio usando el método recognize_google
            try:
                texto = recognice_audio_as_text(audio, recognizer)
                texto = chatgpt(texto,search=True)
                numero_de_palabras = len(texto.split())
                print(texto)
                if 'jarvis' in texto: 
                    texto = texto[texto.find('jarvis'):]
                if texto == 'stop':
                    play_audio("otros",False,contexto="bye")

                    # Liberar recursos
                    recognizer = None
                    stop = False
                elif texto == 'cierra spotify':
                    play_audio("frases")

                    os.system("taskkill /f /im spotify.exe")
                    music_playing = False
                elif texto == 'cierra edge':
                    play_audio("frases")
                    os.system("taskkill /f /im msedge.exe > NUL 2>&1")
                # elif texto.startswith('spotify'): 
                #     if '{nombre y/o datos de la canción}' in texto: 
                #         pass
                #     else:  
                #         new_text = texto.replace('spotify','').replace('reproduce','').strip()
                #         buscar_cancion_spotify(cancion = new_text)
                #         music_playing = True
                elif texto =='cierra pestaña': 
                    keyboard.press_and_release('ctrl+w')
                elif texto == 'abre copilot': 
                    abrir_copilot()
                elif any(word in texto for word in ['busca', 'reproduce', 'youtube', 'search', 'wikipedia']):
                    if len(texto.split()) > 1:  # Asegúrate de que haya una palabra para buscar
                        search_online(texto)
                    else:
                        play_audio("otros",False,contexto="no_especifico_buscar")
                elif texto == 'para musica':
                    detener_reproduccion()
                    music_playing=False
                elif texto == 'pausa video':
                    pausar_continuar_video()
                elif texto.startswith('establecervolumen'): 
                    texto_dividido = texto.split()
                    volumen = int(texto_dividido[1])
                    establecer_volumen(volumen)
                elif texto == 'qué hora es' or texto == 'qué día es hoy' or texto == 'qué día es':
                    date_and_time(texto)
                elif texto == 'toma foto':
                    play_audio("otros", False,contexto="foto")
                    tomar_foto()
                elif texto == 'abre netflix': 
                    abrir_netflix()
                elif texto == 'cierra app': 
                    keyboard.press_and_release('ctrl+w')
                elif texto.startswith('whatsapp'): 
                    palabras = texto.split()
                    enviar_whatsapp(palabras[1])
                elif texto.startswith('analizalaimagen'):
                    audio_nuevo = texto.replace('analizalaimagen', '')
                    chatgpt(audio=audio_nuevo,imagen=True)
                elif is_incomplete_sentence(texto)==True:
                    pass
                elif texto.startswith('jarvis'):
                    new_text = texto.replace('jarvis','')
                    conversation_with_assistant(text=new_text)             
                else: 
                    play_audio("otros",False,contexto="no_entender")
            except Exception as e:
                pass
