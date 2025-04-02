from langchain_community.chat_models import ChatOpenAI
import os

def get_model(temperature=0.3):
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=temperature,
        max_tokens=200,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
