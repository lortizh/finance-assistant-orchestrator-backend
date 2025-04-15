import azure.functions as func
import json
import uuid
from .router_chain import router_chain
from .logging_config import get_logger

# Obtener el logger
logger = get_logger(__name__)

def main(req: func.HttpRequest) -> func.HttpResponse:
    request_id = str(uuid.uuid4())  # Generar un ID único para el seguimiento

    try:
        logger.info(f"[{request_id}] Recibiendo solicitud en el endpoint /orchestrator")

        body = req.get_json()
        user_query = body.get("user_query", "")

        if not user_query:
            logger.error(f"[{request_id}] El campo 'user_query' está vacío")
            return func.HttpResponse(
                json.dumps({"error": "El campo 'user_query' es obligatorio."}),
                status_code=400,
                mimetype="application/json"
            )

        logger.info(f"[{request_id}] Consulta recibida: {user_query}")

        # Llamada al router_chain para enrutar la solicitud
        #response_text = router_chain.run(user_query)

        # --- INICIO DEL CAMBIO ---
        # Si restauraste get_router_chain, descomenta la siguiente línea:
        # current_router_chain = get_router_chain()
        # Si estás usando la instancia global router_chain, usa esa:
        current_router_chain = router_chain

        # Llamada correcta pasando un diccionario con la clave "input"
        response = current_router_chain({"input": user_query})
        # --- FIN DEL CAMBIO ---

        logger.info(f"[{request_id}] Respuesta generada por el router: {response}")

        # Extraer el texto de la respuesta
        if isinstance(response, dict) and "text" in response:
            response_text = response["text"]
        # --- Agregado para manejar el output directo del router ---
        elif isinstance(response, dict) and "output" in response: # A veces MultiPromptChain usa 'output'
             response_text = response["output"]
        # --- Fin agregado ---
        else:
            response_text = str(response) # Fallback

        return func.HttpResponse(
            json.dumps({"response": response_text}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logger.exception(f"[{request_id}] Error interno del servidor")
        return func.HttpResponse(
            json.dumps({"error": f"Error interno: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )
