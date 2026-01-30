"""
임베딩 설정 모듈
"""

from langchain_openai import OpenAIEmbeddings

from src.config import get_settings


def get_embeddings() -> OpenAIEmbeddings:
    """OpenAI 임베딩 인스턴스 반환

    Returns:
        OpenAIEmbeddings 인스턴스
    """
    settings = get_settings()

    return OpenAIEmbeddings(
        model=settings.embedding_model,
        openai_api_key=settings.openai_api_key,
    )
