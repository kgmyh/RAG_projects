"""
Agent 테스트
"""

import pytest
from unittest.mock import patch, MagicMock

from langchain_core.documents import Document

from src.agent.state import AgentState
from src.agent.nodes import retrieve_node, generate_node, grade_node, should_continue


class TestAgentState:
    """AgentState 테스트"""

    def test_state_structure(self):
        """상태 구조 테스트"""
        state: AgentState = {
            "question": "테스트 질문",
            "messages": [],
            "documents": [],
            "answer": None,
            "relevance_score": None,
            "needs_more_search": False,
        }

        assert state["question"] == "테스트 질문"
        assert state["documents"] == []


class TestNodes:
    """노드 함수 테스트"""

    @patch("src.agent.nodes.get_retriever")
    def test_retrieve_node(self, mock_get_retriever):
        """검색 노드 테스트"""
        mock_doc = Document(page_content="테스트 내용", metadata={})
        mock_retriever = MagicMock()
        mock_retriever.invoke.return_value = [mock_doc]
        mock_get_retriever.return_value = mock_retriever

        state: AgentState = {
            "question": "상속세란?",
            "messages": [],
            "documents": [],
            "answer": None,
            "relevance_score": None,
            "needs_more_search": False,
        }

        result = retrieve_node(state)

        assert "documents" in result
        assert len(result["documents"]) == 1

    def test_grade_node_with_documents(self):
        """문서가 있을 때 평가 노드 테스트"""
        docs = [Document(page_content=f"내용 {i}", metadata={}) for i in range(5)]
        state: AgentState = {
            "question": "질문",
            "messages": [],
            "documents": docs,
            "answer": None,
            "relevance_score": None,
            "needs_more_search": False,
        }

        result = grade_node(state)

        assert result["relevance_score"] == 1.0
        assert result["needs_more_search"] == False

    def test_grade_node_without_documents(self):
        """문서가 없을 때 평가 노드 테스트"""
        state: AgentState = {
            "question": "질문",
            "messages": [],
            "documents": [],
            "answer": None,
            "relevance_score": None,
            "needs_more_search": False,
        }

        result = grade_node(state)

        assert result["relevance_score"] == 0.0
        assert result["needs_more_search"] == True

    def test_should_continue_to_generate(self):
        """답변 생성으로 이동 테스트"""
        state: AgentState = {
            "question": "질문",
            "messages": [],
            "documents": [],
            "answer": None,
            "relevance_score": 0.8,
            "needs_more_search": False,
        }

        result = should_continue(state)
        assert result == "generate"

    def test_should_continue_to_retrieve(self):
        """재검색으로 이동 테스트"""
        state: AgentState = {
            "question": "질문",
            "messages": [],
            "documents": [],
            "answer": None,
            "relevance_score": 0.3,
            "needs_more_search": True,
        }

        result = should_continue(state)
        assert result == "retrieve"
