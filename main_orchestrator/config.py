from langchain_community.chat_models import ChatOpenAI
import os

def get_model(temperature):
    return ChatOpenAI(
        model=os.getenv("MODEL_BASE_GPT_TURBO"),
        temperature=temperature,
        max_tokens=200,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
