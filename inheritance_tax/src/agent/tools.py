"""
Agent 도구 정의 모듈
"""

from typing import List

from langchain_core.tools import tool

from src.retriever import get_retriever


@tool
def search_law(query: str) -> str:
    """상속세 및 증여세법에서 관련 내용을 검색합니다.

    Args:
        query: 검색할 법률 관련 질문

    Returns:
        검색된 법률 내용
    """
    retriever = get_retriever(k=5)
    documents = retriever.invoke(query)

    if not documents:
        return "관련 법률 내용을 찾을 수 없습니다."

    results = []
    for i, doc in enumerate(documents, 1):
        results.append(f"[검색결과 {i}]\n{doc.page_content}")

    return "\n\n---\n\n".join(results)


@tool
def get_law_article(article_number: str) -> str:
    """특정 조문 번호로 법률 내용을 검색합니다.

    Args:
        article_number: 조문 번호 (예: "제10조", "제15조의2")

    Returns:
        해당 조문 내용
    """
    retriever = get_retriever(k=3)
    query = f"{article_number} 상속세 증여세"
    documents = retriever.invoke(query)

    if not documents:
        return f"{article_number}를 찾을 수 없습니다."

    # 조문 번호가 포함된 문서 필터링
    filtered_docs = [
        doc for doc in documents
        if article_number in doc.page_content
    ]

    if filtered_docs:
        return filtered_docs[0].page_content
    return documents[0].page_content


def get_tools() -> List:
    """Agent 도구 리스트 반환

    Returns:
        도구 리스트
    """
    return [search_law, get_law_article]
