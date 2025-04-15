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
        "description": "Registro y consulta de ingresos (salarios, pagos) y gastos (compras, pagos). Manejo de montos y categorías. Usar cuando el usuario quiera registrar o consultar movimientos financieros específicos.",
        "prompt_template": prompt_gastos
    },
    {
        "name": "asesoria_financiera",
        "description": "Consejos generales sobre finanzas, inversiones y ahorro. Usar cuando el usuario pida recomendaciones o consejos financieros.",
        "prompt_template": prompt_asesor
    }
]

# Crear el MultiPromptChain
try:
    router_chain = MultiPromptChain.from_prompts(
        llm=chain_gastos.llm,  # Usamos GPT-4 para mejor routing
        prompt_infos=prompt_infos,
        default_chain=chain_gastos,  # Cambiamos el default chain
        verbose=True
    )
    logger.info("Router Chain creado exitosamente")
except Exception as e:
    logger.exception(f"Error al crear el router_chain: {str(e)}")
