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
        "name": "asesoria_financiera",
        "description": "Asesoría financiera sobre inversiones y ahorro.",
        "prompt_template": prompt_asesor
    },
    {
        "name": "control_gastos",
        "description": "Registro y consulta de movimientos financieros.",
        "prompt_template": prompt_gastos
    }
]

# Crear el MultiPromptChain
try:
    router_chain = MultiPromptChain.from_prompts(
        llm=chain_asesor.llm,  # Usamos GPT-3.5 para el router
        prompt_infos=prompt_infos,
        default_chain=chain_asesor,
        verbose=True
    )
    logger.info("Router Chain creado exitosamente")
except Exception as e:
    logger.exception(f"Error al crear el router_chain: {str(e)}")
