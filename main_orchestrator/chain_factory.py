from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from .config import get_model

def create_chain(prompt_text, temperature):
    model = get_model(temperature)
    prompt = PromptTemplate(
        input_variables=["input"],
        template=prompt_text
    )
    return LLMChain(llm=model, prompt=prompt)
