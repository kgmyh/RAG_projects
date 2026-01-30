"""
검색기 테스트
"""

import pytest
from unittest.mock import patch, MagicMock

from langchain_core.documents import Document

from src.retriever.base_retriever import BaseRetriever, get_retriever


class TestBaseRetriever:
    """BaseRetriever 테스트"""

    @patch("src.retriever.base_retriever.QdrantStore")
    def test_init(self, mock_store):
        """초기화 테스트"""
        retriever = BaseRetriever(k=10)
        assert retriever.k == 10

    @patch("src.retriever.base_retriever.QdrantStore")
    def test_get_relevant_documents(self, mock_store_class):
        """문서 검색 테스트"""
        # Mock 설정
        mock_doc = Document(page_content="상속세 관련 내용", metadata={})
        mock_vector_store = MagicMock()
        mock_vector_store.similarity_search.return_value = [mock_doc]

        mock_store_instance = mock_store_class.return_value
        mock_store_instance.get_vector_store.return_value = mock_vector_store

        retriever = BaseRetriever(k=5)
        results = retriever._get_relevant_documents("상속세란?")

        assert len(results) == 1
        assert "상속세" in results[0].page_content


class TestGetRetriever:
    """get_retriever 함수 테스트"""

    @patch("src.retriever.base_retriever.QdrantStore")
    def test_get_retriever(self, mock_store):
        """검색기 생성 테스트"""
        retriever = get_retriever(k=10, score_threshold=0.5)

        assert isinstance(retriever, BaseRetriever)
        assert retriever.k == 10
        assert retriever.score_threshold == 0.5
