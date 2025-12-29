import os
import queue
import sounddevice as sd
import traceback
from dotenv import load_dotenv

from google.cloud import speech_v2
from google.cloud.speech_v2.types import (
    RecognitionConfig,
    StreamingRecognizeRequest,
    ExplicitDecodingConfig,
    StreamingRecognitionConfig
)

from google import genai

# Cargar variables de entorno
load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")
RECOGNIZER_ID = os.getenv("RECOGNIZER_ID")
LOCATION = os.getenv("LOCATION")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./vertexai.json"

# Inicializar cliente Gen AI para Vertex AI
genai_client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION
)

# Parámetros de audio
RATE = 8000
CHANNELS = 1
CHUNK = int(RATE / 10)
audio_q = queue.Queue()

# Contador de feedbacks positivos
feedback_positivo_count = 0

# Callback del micrófono
def audio_callback(indata, frames, time, status):
    if status:
        print("⚠️", status)
    audio_q.put(bytes(indata))

# Función para analizar el sentimiento del texto usando Gemini
def analizar_sentimiento(texto: str) -> str:
    """
    Analiza el sentimiento de un texto usando Gemini AI.
    Retorna: 'positivo', 'negativo' o 'neutral'
    """
    try:
        prompt = f"""Analiza el sentimiento del siguiente texto y responde SOLO con una palabra: 'positivo', 'negativo' o 'neutral'.

Texto: "{texto}"

Respuesta (solo una palabra):"""
        
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        if response and response.text:
            sentimiento = response.text.strip().lower()
            # Validar que la respuesta sea una de las opciones esperadas
            if sentimiento in ['positivo', 'negativo', 'neutral']:
                return sentimiento
            else:
                return 'neutral'  # Por defecto si no reconoce
        return 'neutral'
    except Exception as e:
        print(f"⚠️ Error al analizar sentimiento: {e}")
        return 'neutral'

# Función para traducir texto al inglés usando Gemini
def traducir_a_ingles(texto: str) -> str:
    """
    Traduce un texto en español al inglés usando Gemini AI.
    Retorna el texto traducido.
    """
    try:
        prompt = f"""Traduce el siguiente texto del español al inglés. Responde SOLO con la traducción, sin explicaciones adicionales.

Texto en español: "{texto}"

Traducción al inglés:"""
        
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        if response and response.text:
            return response.text.strip()
        return "[Error en traducción]"
    except Exception as e:
        print(f"⚠️ Error al traducir: {e}")
        return "[Error en traducción]"

# Función para procesar feedback positivo
def procesar_feedback_positivo(texto: str):
    """
    Procesa un feedback positivo: lo traduce al inglés y lo muestra en ambos idiomas.
    También incrementa el contador de feedbacks positivos.
    """
    global feedback_positivo_count
    feedback_positivo_count += 1
    
    print("\n" + "="*60)
    print("✨ ¡FEEDBACK POSITIVO DETECTADO! ✨")
    print("="*60)
    
    # Mostrar en español (original)
    print(f"📝 Español: {texto}")
    
    # Traducir y mostrar en inglés
    print("🔄 Traduciendo al inglés...")
    traduccion = traducir_a_ingles(texto)
    print(f"🌍 English: {traduccion}")
    
    print(f"\n📊 Total de feedbacks positivos registrados: {feedback_positivo_count}")
    print("="*60 + "\n")

# Función para consultar Gemini y obtener respuesta en texto
def responder_con_gemini(texto_usuario: str):
    print("🤖 Escribiendo...")
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Reponda de formar breve y concisa, no más de 100 caracteres: " + texto_usuario
        )
        if response and response.text:
            print(f"🧩 Gemini: {response.text}")
        else:
            print("⚠️ Gemini no devolvió respuesta.")
    except Exception as e:
        print("❌ Error al consultar Gemini:", e)

# Transcripción en streaming con Speech-to-Text v2
def stream_transcription():
    client = speech_v2.SpeechClient()
    recognizer = f"projects/{PROJECT_ID}/locations/global/recognizers/{RECOGNIZER_ID}"

    decoding_config = ExplicitDecodingConfig(
        encoding="LINEAR16",
        sample_rate_hertz=RATE,
        audio_channel_count=CHANNELS,
    )

    config = RecognitionConfig(
        explicit_decoding_config=decoding_config,
        language_codes=["es-GT"],
        model="telephony"
    )

    streaming_config = StreamingRecognitionConfig(config=config)

    def request_generator():
        yield StreamingRecognizeRequest(
            recognizer=recognizer,
            streaming_config=streaming_config,
        )
        while True:
            data = audio_q.get()
            if data is None:
                break
            yield StreamingRecognizeRequest(audio=data)

    print("🎧 Habla con XAIOP. ¿ En qué puedo ayudarte ? (tu asistente IA). Di 'salir' para terminar.")

    try:
        with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype="int16",
                            callback=audio_callback):
            responses = client.streaming_recognize(requests=request_generator())
            for response in responses:
                for result in response.results:
                    if result.alternatives:
                        text = result.alternatives[0].transcript.strip()
                        print(f"🗣️ {text}")
                        if result.is_final:
                            print("✅ Usuario:", text)
                            if "salir" in text.lower():
                                print("\n👋 Fin del asistente por comando de voz. ¡Gracias por usar XAIOP!")
                                print(f"📊 Resumen: Se registraron {feedback_positivo_count} feedbacks positivos en esta sesión.")
                                return
                            
                            # Analizar el sentimiento del texto
                            print("🔍 Analizando sentimiento...")
                            sentimiento = analizar_sentimiento(text)
                            
                            # Mostrar el sentimiento detectado con emoji
                            emoji_sentimiento = {
                                'positivo': '😊',
                                'negativo': '😟',
                                'neutral': '😐'
                            }
                            print(f"{emoji_sentimiento.get(sentimiento, '😐')} Sentimiento detectado: {sentimiento.upper()}")
                            
                            # Si es positivo, procesar como feedback
                            if sentimiento == 'positivo':
                                procesar_feedback_positivo(text)
                            
                            # Responder con Gemini
                            responder_con_gemini(text)
    except KeyboardInterrupt:
        print("\n👋 Finalizado por el usuario.")
    except Exception as e:
        print("❌ Error en streaming:", e)
        traceback.print_exc()

if __name__ == "__main__":
    stream_transcription()
