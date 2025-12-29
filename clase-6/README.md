# 🤖 Asistente de Voz con Gemini AI

## 📋 Descripción

Este proyecto implementa un **asistente de voz inteligente** que combina tecnologías de Google Cloud para crear una experiencia conversacional completa con análisis de sentimiento y registro de feedback bilingüe.

### ¿Qué hace `asistente-gemini.py`?

El script crea un asistente de voz que:

1. **Escucha tu voz** en tiempo real a través del micrófono
2. **Transcribe** lo que dices usando Google Cloud Speech-to-Text V2
3. **Analiza el sentimiento** de tus comentarios (positivo, negativo o neutral)
4. **Registra feedbacks positivos** en español e inglés automáticamente
5. **Responde inteligentemente** usando Gemini AI
6. **Mantiene un contador** de todos los feedbacks positivos de la sesión

---

## 🎯 Características Principales

### 1. **Transcripción de Voz en Tiempo Real**
- Captura audio del micrófono continuamente
- Transcribe a texto usando Speech-to-Text V2
- Modelo optimizado para voz telefónica (8kHz)
- Soporte para español (es-GT)

### 2. **Análisis de Sentimiento con IA**
- Clasifica automáticamente cada comentario como:
  - 😊 **Positivo**: Comentarios felices, agradecimientos, satisfacción
  - 😟 **Negativo**: Quejas, frustración, insatisfacción
  - 😐 **Neutral**: Preguntas, información general

### 3. **Sistema de Feedback Bilingüe**
- Detecta automáticamente comentarios positivos
- Traduce del español al inglés usando Gemini AI
- Muestra ambas versiones en la consola
- Registra un contador de feedbacks positivos

### 4. **Respuestas Inteligentes**
- Gemini AI genera respuestas contextuales
- Respuestas concisas (máximo 100 caracteres)
- Conversación natural y fluida

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Propósito |
|------------|-----------|
| **Google Cloud Speech V2** | Transcripción de voz a texto |
| **Gemini AI (2.5 Flash)** | Análisis de sentimiento, traducción y respuestas |
| **Vertex AI** | Plataforma de ML/AI de Google Cloud |
| **sounddevice** | Captura de audio del micrófono |
| **Python 3.12** | Lenguaje de programación |

---

## 📦 Requisitos

### Dependencias del Sistema
```bash
# En Linux (Ubuntu/Debian)
sudo apt-get install libasound2-dev

# En macOS
brew install portaudio
```

### Dependencias de Python
```bash
pip install -r requirements.txt
```

**Archivo `requirements.txt`:**
```
google-cloud-speech==2.34.0
google-cloud-texttospeech==2.33.0
google-cloud-aiplatform==1.124.0
sounddevice==0.5.3
numpy==2.3.4
python-dotenv==1.2.1
simpleaudio==1.0.4
```

### Configuración de Google Cloud

1. **Crear un proyecto en Google Cloud**
2. **Habilitar las APIs:**
   - Cloud Speech-to-Text API
   - Vertex AI API
3. **Crear un recognizer en Speech V2:**
   ```bash
   gcloud speech recognizers create myrecognizer-datapath-demo \
     --location=global \
     --model=telephony \
     --language-codes=es-GT
   ```
4. **Crear credenciales de servicio** y descargar `vertexai.json`
5. **Configurar archivo `.env`:**
   ```env
   PROJECT_ID=tu-project-id
   RECOGNIZER_ID=myrecognizer-datapath-demo
   LOCATION=us-central1
   ```

---

## 🚀 Uso

### Iniciar el Asistente

```bash
# Activar entorno virtual
source .venv/bin/activate

# Ejecutar el asistente
python asistente-gemini.py
```

### Comandos de Voz

- **"salir"** - Termina el asistente y muestra resumen de feedbacks
- **Cualquier pregunta** - El asistente responderá usando Gemini AI
- **Comentarios positivos** - Se registrarán automáticamente en español e inglés

---

## 💬 Ejemplos de Output en Terminal

### Ejemplo 1: Feedback Positivo

```
🎧 Habla con XAIOP. ¿ En qué puedo ayudarte ? (tu asistente IA). Di 'salir' para terminar.

🗣️ Estoy muy contento con este asistente
✅ Usuario: Estoy muy contento con este asistente
🔍 Analizando sentimiento...
😊 Sentimiento detectado: POSITIVO

============================================================
✨ ¡FEEDBACK POSITIVO DETECTADO! ✨
============================================================
📝 Español: Estoy muy contento con este asistente
🔄 Traduciendo al inglés...
🌍 English: I am very happy with this assistant

📊 Total de feedbacks positivos registrados: 1
============================================================

🤖 Escribiendo...
🧩 Gemini: ¡Me alegra mucho escuchar eso! ¿En qué más puedo ayudarte?
```

### Ejemplo 2: Pregunta Normal (Neutral)

```
🗣️ ¿Cuál es la capital de Francia?
✅ Usuario: ¿Cuál es la capital de Francia?
🔍 Analizando sentimiento...
😐 Sentimiento detectado: NEUTRAL
🤖 Escribiendo...
🧩 Gemini: París es la capital de Francia.
```

### Ejemplo 3: Comentario Negativo

```
🗣️ No entiendo nada de esto
✅ Usuario: No entiendo nada de esto
🔍 Analizando sentimiento...
😟 Sentimiento detectado: NEGATIVO
🤖 Escribiendo...
🧩 Gemini: Tranquilo, vamos paso a paso. ¿Qué parte específica te confunde?
```

### Ejemplo 4: Múltiples Feedbacks Positivos

```
🗣️ Me encanta cómo funciona
✅ Usuario: Me encanta cómo funciona
🔍 Analizando sentimiento...
😊 Sentimiento detectado: POSITIVO

============================================================
✨ ¡FEEDBACK POSITIVO DETECTADO! ✨
============================================================
📝 Español: Me encanta cómo funciona
🔄 Traduciendo al inglés...
🌍 English: I love how it works

📊 Total de feedbacks positivos registrados: 2
============================================================

🤖 Escribiendo...
🧩 Gemini: ¡Excelente! Me alegra que te guste.

🗣️ Gracias por tu ayuda
✅ Usuario: Gracias por tu ayuda
🔍 Analizando sentimiento...
😊 Sentimiento detectado: POSITIVO

============================================================
✨ ¡FEEDBACK POSITIVO DETECTADO! ✨
============================================================
📝 Español: Gracias por tu ayuda
🔄 Traduciendo al inglés...
🌍 English: Thank you for your help

📊 Total de feedbacks positivos registrados: 3
============================================================

🤖 Escribiendo...
🧩 Gemini: ¡De nada! Siempre a tu disposición.
```

### Ejemplo 5: Salir del Asistente

```
🗣️ salir
✅ Usuario: salir

👋 Fin del asistente por comando de voz. ¡Gracias por usar XAIOP!
📊 Resumen: Se registraron 3 feedbacks positivos en esta sesión.
```

---

## 📊 Flujo de Funcionamiento

```
1. Micrófono captura audio (8kHz, mono)
   ↓
2. Speech API transcribe en tiempo real
   ↓
3. Transcripción final detectada
   ↓
4. Gemini analiza el sentimiento
   ↓
5. ¿Es positivo?
   ├─ SÍ → Registra feedback bilingüe (ES/EN)
   └─ NO → Continúa
   ↓
6. Gemini genera respuesta inteligente
   ↓
7. Muestra respuesta en consola
   ↓
8. Vuelve al paso 1 (hasta decir "salir")
```

---

## 🎓 Conceptos Técnicos Implementados

### 1. **Streaming de Audio**
- Captura continua mediante callbacks asíncronos
- Queue thread-safe para comunicación entre threads
- Chunks de 100ms para baja latencia

### 2. **Análisis de Sentimiento (NLP)**
- Clasificación automática de emociones en texto
- Prompt engineering para respuestas consistentes
- Aplicación práctica de procesamiento de lenguaje natural

### 3. **Traducción Automática Neural**
- Gemini AI como motor de traducción
- Procesamiento contextual (no literal)
- Traducción español → inglés en tiempo real

### 4. **Prompt Engineering**
- Instrucciones específicas para Gemini
- Validación de respuestas esperadas
- Optimización de outputs de IA

### 5. **Generator Pattern**
- Streaming de datos sin bloquear el programa
- Yield para envío continuo de audio
- Eficiencia en uso de memoria

---

## 📁 Estructura del Proyecto

```
clase-6/
├── asistente-gemini.py      # Script principal del asistente
├── main.py                   # Script básico (solo transcripción)
├── requirements.txt          # Dependencias de Python
├── .env                      # Variables de entorno (no incluido en git)
├── vertexai.json            # Credenciales de Google Cloud (no incluido en git)
├── .gitignore               # Archivos ignorados por git
├── Taskfile.yml             # Automatización de tareas
├── docs/
│   ├── diagram-main.html            # Documentación visual de main.py
│   └── diagram-asistente-gemini.html # Documentación visual del asistente
└── README.md                # Este archivo
```

---

## 🔧 Uso con Taskfile

Este proyecto incluye un `Taskfile.yml` para automatizar tareas comunes:

```bash
# Crear entorno virtual
task create-venv

# Instalar dependencias
task install-deps

# Ejecutar el asistente
task run

# Configuración completa (venv + deps)
task setup

# Limpiar entorno virtual
task clean
```

---

## 🐛 Solución de Problemas

### Error: "No module named 'sounddevice'"
```bash
# Asegúrate de activar el entorno virtual
source .venv/bin/activate
pip install -r requirements.txt
```

### Error: "alsa/asoundlib.h: No such file or directory"
```bash
# Instala las dependencias del sistema
sudo apt-get install libasound2-dev
```

### Error: "Unable to find Recognizer"
```bash
# Verifica que el recognizer existe en Google Cloud
gcloud speech recognizers list --location=global

# Crea uno si no existe
gcloud speech recognizers create myrecognizer-datapath-demo \
  --location=global \
  --model=telephony \
  --language-codes=es-GT
```

### Error: "Expected resource location to be global"
- El recognizer debe estar en la ubicación `global` para streaming
- Verifica que en el código uses: `locations/global/recognizers/...`

---

## 📈 Casos de Uso

### 1. **Atención al Cliente**
- Registro automático de satisfacción del cliente
- Análisis de sentimiento en tiempo real
- Métricas de feedback positivo/negativo

### 2. **Asistente Personal**
- Respuestas a preguntas generales
- Conversación natural con IA
- Interfaz de voz manos libres

### 3. **Educación**
- Aprendizaje de conceptos de IA y NLP
- Práctica con APIs de Google Cloud
- Implementación de sistemas conversacionales

### 4. **Análisis de Feedback**
- Recopilación automática de comentarios
- Traducción para análisis global
- Estadísticas de satisfacción

---

## 🔐 Seguridad

- **NO** subas `vertexai.json` a repositorios públicos
- **NO** compartas tu archivo `.env`
- Usa `.gitignore` para excluir archivos sensibles
- Rota las credenciales periódicamente

---

## 📝 Diferencias entre Scripts

| Característica | main.py | asistente-gemini.py |
|----------------|---------|---------------------|
| Transcripción | ✅ | ✅ |
| Análisis de Sentimiento | ❌ | ✅ |
| Feedback Bilingüe | ❌ | ✅ |
| Respuestas con Gemini | ❌ | ✅ |
| Traducción Automática | ❌ | ✅ |
| Contador de Feedbacks | ❌ | ✅ |

---

## 🤝 Contribuciones

Este proyecto es parte del curso de IA de Datapath. Para mejoras o sugerencias, contacta al instructor.

---

## 📄 Licencia

Proyecto educativo - Datapath Curso IA

---

## 👨‍💻 Autor

Desarrollado por Oscar Llamas como parte del curso de Inteligencia Artificial - Clase 6

---

## 🔗 Enlaces Útiles

- [Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Gemini AI](https://ai.google.dev/)
- [sounddevice Documentation](https://python-sounddevice.readthedocs.io/)

---

## 📞 Soporte

Para problemas técnicos o preguntas sobre el proyecto, consulta:
1. La documentación visual en `docs/diagram-asistente-gemini.html`
2. Los ejemplos de output en este README
3. Los comentarios en el código fuente
