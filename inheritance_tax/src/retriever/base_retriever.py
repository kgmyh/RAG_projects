"""
기본 검색기 모듈
- Qdrant 벡터 스토어를 사용한 문서 검색 기능 제공
"""

# 타입 힌트를 위한 모듈 임포트
from typing import List, Optional

# LangChain 문서 객체 - 검색 결과를 담는 데이터 구조
from langchain_core.documents import Document
# LangChain 기본 검색기 추상 클래스 - 커스텀 검색기 구현을 위한 베이스
from langchain_core.retrievers import BaseRetriever as LangChainBaseRetriever
# 콜백 매니저 - 검색 과정 모니터링 및 로깅용
from langchain_core.callbacks import CallbackManagerForRetrieverRun

# Qdrant 벡터 스토어 관리 클래스 임포트
from src.vectorstore.qdrant_store import QdrantStore


class BaseRetriever(LangChainBaseRetriever):
    """기본 벡터 검색기
    
    LangChain의 BaseRetriever를 상속받아 Qdrant 기반 검색 구현
    """

    # 클래스 속성 정의
    vector_store: QdrantStore = None  # Qdrant 벡터 스토어 인스턴스
    k: int = 5  # 반환할 검색 결과 개수 (기본값: 5개)
    score_threshold: Optional[float] = None  # 최소 유사도 점수 임계값

    class Config:
        # Pydantic 설정: 커스텀 타입(QdrantStore) 허용
        arbitrary_types_allowed = True

    def __init__(
        self,
        k: int = 5,  # 검색할 문서 수
        score_threshold: Optional[float] = None,  # 최소 유사도 점수 (None이면 필터링 없음)
        **kwargs,  # 추가 키워드 인자
    ):
        """
        Args:
            k: 검색할 문서 수
            score_threshold: 최소 유사도 점수
        """
        # 부모 클래스 초기화 호출
        super().__init__(**kwargs)
        # Qdrant 벡터 스토어 인스턴스 생성
        self.vector_store = QdrantStore()
        # 검색 결과 개수 설정
        self.k = k
        # 유사도 점수 임계값 설정
        self.score_threshold = score_threshold

    def _get_relevant_documents(
        self,
        query: str,  # 사용자 검색 쿼리
        *,
        run_manager: Optional[CallbackManagerForRetrieverRun] = None,  # 콜백 매니저 (선택적)
    ) -> List[Document]:
        """관련 문서 검색
        
        쿼리와 유사한 문서를 벡터 DB에서 검색하여 반환

        Args:
            query: 검색 쿼리
            run_manager: 콜백 매니저

        Returns:
            관련 문서 리스트
        """
        # Qdrant 벡터 스토어 인스턴스 가져오기
        qdrant_vs = self.vector_store.get_vector_store()

        # 유사도 점수 임계값이 설정된 경우
        if self.score_threshold:
            # 유사도 점수와 함께 검색 수행
            docs = qdrant_vs.similarity_search_with_score(
                query=query,  # 검색할 쿼리
                k=self.k,  # 검색 결과 개수
            )
            # 점수 필터링: 임계값 이상인 문서만 선택
            filtered_docs = [
                doc for doc, score in docs if score >= self.score_threshold
            ]
            # 필터링된 문서 리스트 반환
            return filtered_docs
        else:
            # 점수 필터링 없이 단순 유사도 검색 수행
            return qdrant_vs.similarity_search(
                query=query,  # 검색할 쿼리
                k=self.k,  # 검색 결과 개수
            )


def get_retriever(
    k: int = 5,  # 검색할 문서 수 (기본값: 5)
    score_threshold: Optional[float] = None,  # 최소 유사도 점수 (기본값: None)
) -> BaseRetriever:
    """검색기 인스턴스 반환
    
    BaseRetriever 객체를 생성하여 반환하는 팩토리 함수

    Args:
        k: 검색할 문서 수
        score_threshold: 최소 유사도 점수

    Returns:
        BaseRetriever 인스턴스
    """
    # 설정된 파라미터로 BaseRetriever 인스턴스 생성 및 반환
    return BaseRetriever(k=k, score_threshold=score_threshold)
