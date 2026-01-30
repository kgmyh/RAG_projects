"""
하이브리드 검색기 모듈 (향후 확장용)
"""

from typing import List, Optional

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever as LangChainBaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun

from src.retriever.base_retriever import BaseRetriever


class HybridRetriever(LangChainBaseRetriever):
    """하이브리드 검색기 (벡터 검색 + 키워드 검색)

    향후 BM25 등 키워드 검색을 결합한 하이브리드 검색 구현용
    """

    vector_retriever: BaseRetriever = None
    k: int = 5
    vector_weight: float = 0.7

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        k: int = 5,
        vector_weight: float = 0.7,
        **kwargs,
    ):
        """
        Args:
            k: 검색할 문서 수
            vector_weight: 벡터 검색 가중치 (0-1)
        """
        super().__init__(**kwargs)
        self.vector_retriever = BaseRetriever(k=k)
        self.k = k
        self.vector_weight = vector_weight

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: Optional[CallbackManagerForRetrieverRun] = None,
    ) -> List[Document]:
        """관련 문서 검색

        현재는 벡터 검색만 사용, 향후 키워드 검색 결합 예정

        Args:
            query: 검색 쿼리
            run_manager: 콜백 매니저

        Returns:
            관련 문서 리스트
        """
        # 현재는 벡터 검색만 사용
        vector_docs = self.vector_retriever.invoke(query)

        # TODO: 키워드 검색 결합
        # keyword_docs = self._keyword_search(query)
        # merged_docs = self._merge_results(vector_docs, keyword_docs)

        return vector_docs[:self.k]
