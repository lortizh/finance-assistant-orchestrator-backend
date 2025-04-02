from .chain_factory import create_chain
from .prompts import prompt_asesor
from .logging_config import get_logger

# Obtener el logger configurado
logger = get_logger(__name__)

# Crear el chain para el asesor financiero
chain_asesor = create_chain(prompt_asesor, temperature=0.7)

def process_advice_response(response):
    """Formatea y valida la respuesta del asesor financiero"""
    try:
        logger.debug(f"Respuesta cruda del asesor: {response}")

        # Procesar la respuesta para eliminar espacios en blanco
        data = response.strip()
        if not data:
            logger.warning("La respuesta del asesor está vacía o no contiene información útil.")
            return {"status": "error", "message": "No se pudo generar una respuesta de asesoría"}

        logger.info(f"Respuesta procesada del asesor: {data}")
        return {"status": "success", "response": data}

    except Exception as e:
        logger.exception("Error al procesar la respuesta del asesor financiero")
        return {"status": "error", "message": f"Error al procesar la respuesta: {str(e)}"}

# Log de inicialización del agente
logger.info("Agente de asesoría financiera inicializado correctamente")
