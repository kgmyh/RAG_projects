"""
Agent 상태 정의 모듈
"""

from typing import List, Optional, Annotated
from typing_extensions import TypedDict

from langchain_core.documents import Document
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """Agent 상태 정의"""

    # 사용자 질문
    question: str

    # 대화 히스토리
    messages: Annotated[list, add_messages]

    # 검색된 문서
    documents: List[Document]

    # 생성된 답변
    answer: Optional[str]

    # 문서 관련성 점수
    relevance_score: Optional[float]

    # 추가 검색 필요 여부
    needs_more_search: bool
