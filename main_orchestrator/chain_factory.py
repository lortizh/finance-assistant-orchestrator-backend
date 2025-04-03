from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from .config import get_model, get_gpt4_model, get_gpt35_model

def create_chain(prompt_text, temperature=0.3, use_gpt4=False):
    """
    Crea una cadena de procesamiento.
    Args:
        prompt_text (str): El texto del prompt
        temperature (float): Nivel de creatividad
        use_gpt4 (bool): Si se debe usar GPT-4 en lugar de GPT-3.5
    """
    model = get_gpt4_model(temperature) if use_gpt4 else get_gpt35_model(temperature)
    prompt = PromptTemplate(
        input_variables=["input"],
        template=prompt_text
    )
    return LLMChain(llm=model, prompt=prompt)
