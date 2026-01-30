"""
Agent 그래프 노드 모듈
"""

from typing import Dict, Any

from langchain_core.documents import Document

from src.agent.state import AgentState
from src.retriever import get_retriever
from src.chain import get_rag_chain


def retrieve_node(state: AgentState) -> Dict[str, Any]:
    """문서 검색 노드

    Args:
        state: 현재 Agent 상태

    Returns:
        업데이트된 상태 딕셔너리
    """
    question = state["question"]
    retriever = get_retriever(k=5)

    documents = retriever.invoke(question)

    return {
        "documents": documents,
    }


def generate_node(state: AgentState) -> Dict[str, Any]:
    """답변 생성 노드

    Args:
        state: 현재 Agent 상태

    Returns:
        업데이트된 상태 딕셔너리
    """
    question = state["question"]
    documents = state["documents"]

    rag_chain = get_rag_chain()

    # 문서 내용 결합
    context = "\n\n".join([doc.page_content for doc in documents])

    answer = rag_chain.invoke({
        "question": question,
        "context": context,
    })

    return {
        "answer": answer,
    }


def grade_node(state: AgentState) -> Dict[str, Any]:
    """문서 관련성 평가 노드

    Args:
        state: 현재 Agent 상태

    Returns:
        업데이트된 상태 딕셔너리
    """
    documents = state["documents"]

    # 간단한 관련성 점수 계산 (문서 수 기반)
    if not documents:
        relevance_score = 0.0
        needs_more_search = True
    elif len(documents) < 3:
        relevance_score = 0.5
        needs_more_search = True
    else:
        relevance_score = 1.0
        needs_more_search = False

    return {
        "relevance_score": relevance_score,
        "needs_more_search": needs_more_search,
    }


def should_continue(state: AgentState) -> str:
    """조건부 엣지: 계속 진행 여부 결정

    Args:
        state: 현재 Agent 상태

    Returns:
        다음 노드 이름
    """
    if state.get("needs_more_search", False) and state.get("relevance_score", 0) < 0.5:
        return "retrieve"
    return "generate"
