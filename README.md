# 🧠 Asistente Jarvis

Asistente virtual activado por voz con integración de APIs, procesamiento de lenguaje natural, control del sistema y automatización de tareas cotidianas.

---

## 🚀 Características principales

- 🎙️ Reconocimiento de voz con palabras clave (Jarvis, Picovoice)
- 🗣️ Text-to-speech con ElevenLabs
- 🧠 Procesamiento con OpenAI GPT (modo conversación y comandos rápidos)
- 📸 Toma de fotos y detección de rostros (OpenCV)
- 🔊 Control de volumen y reproducción de Spotify / videos
- 🌐 Búsquedas en Google y YouTube
- 📱 Envío de mensajes por WhatsApp
- 📦 Modular y fácil de extender

---

## 📦 Requisitos

- Python 3.8+

Instalación de dependencias (usa `pyproject.toml`):
```bash
pip install .
```

O usando Poetry:
```bash
poetry install
```

---

## 🔐 Configuración

1. Crea un archivo `.env` en la raíz del proyecto:

```
ELEVENLABS_API_KEY=tu_clave_de_elevenlabs_aqui
```

2. Asegúrate de tener también tus modelos HaarCascade en `docs/modelos`

3. Guarda tus audios personalizados en `docs/audios` y las fotos capturadas se almacenarán en `docs/fotos`

---

## 🧪 Cómo usar

Desde consola:
```bash
python main.py
```

El asistente esperará una palabra clave como "Jarvis" o "Picovoice". Una vez activado, podrás interactuar con comandos como:

- "¿Qué hora es?"
- "Toma una foto"
- "Busca gatos en Google"
- "Reproduce Coldplay en Spotify"
- "Envía un WhatsApp a mamá"
- "Jarvis, ¿qué opinas del cambio climático?"

---

## 📁 Estructura del proyecto

```
asistente-jarvis/
├── docs/
│   ├── audios/
│   ├── fotos/
│   └── modelos/
├── funciones.py
├── main.py
├── variables_gobales.py
├── .env
├── pyproject.toml
└── README.md
```





