from langchain_community.chat_models import ChatOpenAI
import os

def get_model(temperature=0.3, model_name=None):
    """
    Obtiene una instancia del modelo de lenguaje.
    Args:
        temperature (float): Nivel de creatividad del modelo
        model_name (str): Nombre del modelo a usar (gpt-4 o gpt-3.5-turbo)
    """
    # Si no se especifica modelo, usar el default de las variables de entorno
    if not model_name:
        model_name = os.getenv("MODEL_BASE_GPT_TURBO", "gpt-3.5-turbo")
    
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=200,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

# Funciones específicas para diferentes casos de uso
def get_gpt4_model(temperature=0.3):
    """Obtiene una instancia específica de GPT-4"""
    return get_model(temperature=temperature, model_name="gpt-4")

def get_gpt35_model(temperature=0.3):
    """Obtiene una instancia específica de GPT-3.5"""
    return get_model(temperature=temperature, model_name="gpt-3.5-turbo")
