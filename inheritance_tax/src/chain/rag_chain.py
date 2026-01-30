"""
RAG 체인 구성 모듈
"""

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.config import get_settings
from src.chain.prompts import get_rag_prompt


def get_llm() -> ChatOpenAI:
    """LLM 인스턴스 반환

    Returns:
        ChatOpenAI 인스턴스
    """
    settings = get_settings()

    return ChatOpenAI(
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        openai_api_key=settings.openai_api_key,
    )


def get_rag_chain():
    """RAG 체인 반환

    Returns:
        RAG 체인 인스턴스
    """
    prompt = get_rag_prompt()
    llm = get_llm()
    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser

    return chain


def get_rag_chain_with_retriever(retriever):
    """검색기가 포함된 RAG 체인 반환

    Args:
        retriever: 문서 검색기

    Returns:
        RAG 체인 인스턴스
    """
    prompt = get_rag_prompt()
    llm = get_llm()
    output_parser = StrOutputParser()

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | output_parser
    )

    return chain
