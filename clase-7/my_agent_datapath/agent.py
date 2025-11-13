import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search, agent_tool
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

#Autenticación
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../clase-7/cuenta-servicio.json'
RAG_CORPUS= os.environ.get("RAG_CORPUS")  # p.ej. "projects/xxx/locations/us-central1/ragCorpora/id-corpus"

model = "gemini-2.5-flash"
model_live = "gemini-live-2.5-flash-preview-native-audio-09-2025"

# === Subagentes ===

saludo_agent = Agent(
    model=model,
    name='agente_saludo',
    description='Responde saludos cordiales y se presenta de forma amigable.',
    instruction='Responde de manera amable y corta a saludos como "hola", "buenos días", "qué tal", etc. Usa emojis 😄.'
)

vuelos_agent = Agent(
    model=model,
    name='agente_vuelos',
    description='Busca y proporciona información sobre vuelos.',
    instruction=(
        'Eres un asistente experto en encontrar vuelos y hoteles. '
        'Usa la herramienta de búsqueda para encontrar opciones económicas y mejor calificadas. '
        'Devuelve un resumen conciso (máx. 100 palabras) con la mejor opción, precio, aerolínea y fecha.'
    ),
    tools=[google_search]
)

restaurantes_agent = Agent(
    model=model,
    name='agente_restaurantes',
    description='Busca y proporciona información sobre restaurantes.',
    instruction=(
        'Eres un asistente experto en encontrar restaurantes. '
        'Usa la herramienta de búsqueda para encontrar opciones económicas y mejor calificadas. '
        'Devuelve un resumen conciso (máx. 100 palabras) con la mejor opción, precio, ubicación y tipo de cocina.'
    ),
    tools=[google_search]
)

# === Herramienta RAG ===

ask_vertex_retrieval = VertexAiRagRetrieval(
    name='rag-corpus-restaurantes-vuelos-colombia',
    description='Recupera información del corpus RAG sobre vuelos y restaurantes en Colombia.',
    rag_resources=[
        rag.RagResource(
            rag_corpus=RAG_CORPUS
        )
    ],
    similarity_top_k=10,  # Dame los 10 documentos más prometedores para empezar a trabajar.
    vector_distance_threshold=0.4,  # De los 10 documentos, quédate únicamente con aquellos cuya distancia a mi pregunta sea menor que 0.4. Entre menor sea es muy estricto
)

rag_agent = Agent(
    model=model,
    name="agente_rag",
    description="Recupera información del corpus RAG sobre vuelos y restaurantes.",
    instruction="Usa esta herramienta para recuperar información del corpus RAG antes de invocar otros agentes.",
    tools=[ask_vertex_retrieval],
)

# === Agente principal (root) ===

root_agent = Agent(
    model=model,
    name='root_agent',
    description='Agente orquestador que decide qué subagente debe responder. Siempre consulta primero la base de conocimiento (RAG) antes de decidir.',
    instruction=("""
                Eres el agente orquestador principal. Tu única función es gestionar la consulta del usuario siguiendo ESTRICTAMENTE los siguientes pasos en este orden exacto:

                Paso 1: OBTENER CONTEXTO INTERNO (OBLIGATORIO)
                - Ante CUALQUIER consulta del usuario, tu primer y OBLIGATORIO paso es invocar siempre al 'agente_rag'.
                - El objetivo es buscar información y contexto relevante en la base de conocimientos interna ANTES de hacer cualquier otra cosa.
                - NUNCA te saltes este paso.

                Paso 2: ANALIZAR Y DECIDIR LA DELEGACIÓN
                - Una vez que tengas la respuesta del 'agente_rag', analiza la consulta original del usuario Y la información recuperada.
                - A) Si la información de 'agente_rag' es suficiente para responder de forma completa y precisa, formula la respuesta final usando solo esa información y no llames a ningún otro agente.
                - B) Si la información de 'agente_rag' es insuficiente, está incompleta o la consulta requiere datos en tiempo real (como precios de vuelos actuales), DELEGA la consulta al subagente más adecuado según estas reglas:
                    - Para saludos ('hola', 'qué tal', 'buenos días'): usa 'agente_saludo'.
                    - Para buscar vuelos, aerolíneas o billetes de avión: usa 'agente_vuelos'.
                    - Para buscar restaurantes, comida o lugares para comer: usa 'agente_restaurantes'.

                Paso 3: SINTETIZAR Y RESPONDER
                - Si delegaste a un subagente en el paso 2, toma su resultado y combínalo con el contexto que obtuviste del 'agente_rag' en el paso 1.
                - Tu responsabilidad final es consolidar toda la información relevante (de RAG y/o del subagente especialista) en una única respuesta coherente y bien formateada para el usuario.
                - Nunca respondas con la salida cruda de un subagente; siempre intégrala.
                """
    ),
    tools=[
        agent_tool.AgentTool(agent=rag_agent),
        agent_tool.AgentTool(agent=saludo_agent),
        agent_tool.AgentTool(agent=vuelos_agent),
        agent_tool.AgentTool(agent=restaurantes_agent),
    ],
)



