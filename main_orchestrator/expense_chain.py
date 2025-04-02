from .chain_factory import create_chain
from .prompts import prompt_gastos
from .logging_config import get_logger

logger = get_logger(__name__)

# Crear el chain para el control de gastos
chain_control_gastos = create_chain(prompt_gastos, temperature=0.3)

def process_expense_response(response):
    """Formatea y valida la respuesta del agente de gastos"""
    logger.debug(f"Respuesta sin procesar: {response}")
    try:
        data = response.strip()
        if not data:
            logger.warning("Respuesta del agente de gastos está vacía")
            return {"status": "error", "message": "No se pudo procesar el gasto"}
        logger.info(f"Respuesta del agente de gastos procesada: {data}")
        return {"status": "success", "response": data}
    except Exception as e:
        logger.exception("Error al procesar la respuesta del agente de gastos")
        return {"status": "error", "message": f"Error al procesar: {str(e)}"}
