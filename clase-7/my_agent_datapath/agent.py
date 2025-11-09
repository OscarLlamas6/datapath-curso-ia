import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search,agent_tool

# 🔐 Autenticación
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../clase-7/cuenta-servicio.json'

model="gemini-2.5-flash"
model_live="gemini-live-2.5-flash-preview-native-audio-09-2025"


# Agente de saludo
greeting_agent = Agent(
    model=model,
    name='agente_saludo',
    description='Un agente especializado en responder saludos cordiales y presentarse de forma amigable.',
    instruction='Responde de manera amable y corta a saludos como "hola", "buenos días", "qué tal", etc, utiliza emojics'
)

# Agente de vuelos
vuelos_agent = Agent(
    model=model,
    name='agente_vuelos',
    description='Un agente especializado en buscar y proporcionar información sobre vuelos.',
    instruction=
        'Eres un asistente experto en encontrar vuelos y hoteles. '
        'Usa la herramienta de búsqueda para encontrar las opciones más económicas y mejor calificadas. '
        'Devuelve un resumen conciso con la mejor opción y los factores clave (precio, aerolínea, fecha o calificación) '
        'responda de forma breve sin entrar en detalles, maximo 100 palabras.',
    tools=[google_search]
)

# Agente de restaurantes
restaurantes_agent = Agent(
    model=model,
    name='agente_restaurantes',
    description='Un agente especializado en buscar y proporcionar información sobre restaurantes.',
    instruction=
        'Eres un asistente experto en encontrar restaurantes. '
        'Usa la herramienta de búsqueda para encontrar las opciones más económicas y mejor calificadas. '
        'Devuelve un resumen conciso con la mejor opción y los factores clave (precio, ubicación, tipo de cocina) '
        'responda de forma breve sin entrar en detalles, maximo 100 palabras.',
    tools=[google_search]
)


root_agent = Agent(
    model=model,
    name='root_agent',
    description='Agente principal que enruta mensajes a los subagentes.',
    instruction='Dirige el mensaje al subagente adecuado según el contexto (saludo, vuelos o restaurantes).',
    tools=[agent_tool.AgentTool(agent=greeting_agent), agent_tool.AgentTool(agent=vuelos_agent), agent_tool.AgentTool(agent=restaurantes_agent)]
)




