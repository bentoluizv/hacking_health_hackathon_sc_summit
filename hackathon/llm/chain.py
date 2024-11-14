from langchain_cohere import ChatCohere

from hackathon.settings import get_settings

settings = get_settings()


def get_llm():
    llm = ChatCohere(
        model='command-r-plus', cohere_api_key=settings.COHERE_API_KEY
    )

    return llm
