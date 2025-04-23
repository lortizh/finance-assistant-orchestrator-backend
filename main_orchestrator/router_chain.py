from langchain_community.chat_models import ChatOpenAI
from langchain.chains.router import MultiPromptChain
from .chain_factory import create_chain
from .prompts import prompt_asesor, prompt_gastos
from .logging_config import get_logger

logger = get_logger(__name__)

# Crear sub-chains
chain_asesor = create_chain(prompt_asesor, temperature=0.7, use_gpt4=False)  # GPT-3.5 para asesoría
chain_gastos = create_chain(prompt_gastos, temperature=0.0, use_gpt4=True)   # GPT-4 para gastos

# Información del enrutador
prompt_infos = [
    {
        "name": "control_gastos",
        "description": "Útil para registrar o consultar transacciones financieras específicas: ingresos (salarios, pagos recibidos), gastos (compras, pagos realizados), movimientos. Requiere detalles como montos, categorías.",
        "prompt_template": prompt_gastos
    },
    {
        "name": "asesoria_financiera",
        "description": "Útil para consejos generales sobre finanzas, inversiones, ahorros, planificación financiera, o para responder a saludos y preguntas generales no transaccionales.",
        "prompt_template": prompt_asesor
    }
]

# Crear el MultiPromptChain
try:
    router_chain = MultiPromptChain.from_prompts(
        llm=chain_gastos.llm,  # Mantenemos GPT-4 para el routing
        prompt_infos=prompt_infos,
        default_chain=chain_asesor,  # Cambiamos el default al asesor
        verbose=True
    )
    logger.info("Router Chain creado exitosamente con default=asesor")
except Exception as e:
    logger.exception(f"Error al crear el router_chain: {str(e)}")
