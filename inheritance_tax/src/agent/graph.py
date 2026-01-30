"""
LangGraph 워크플로우 모듈
"""

from langgraph.graph import StateGraph, END

from src.agent.state import AgentState
from src.agent.nodes import retrieve_node, generate_node, grade_node, should_continue


def create_agent_graph() -> StateGraph:
    """Agent 그래프 생성

    Returns:
        컴파일된 StateGraph
    """
    # 그래프 생성
    workflow = StateGraph(AgentState)

    # 노드 추가
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("grade", grade_node)
    workflow.add_node("generate", generate_node)

    # 엣지 설정
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "grade")

    # 조건부 엣지
    workflow.add_conditional_edges(
        "grade",
        should_continue,
        {
            "retrieve": "retrieve",
            "generate": "generate",
        },
    )

    workflow.add_edge("generate", END)

    return workflow.compile()


def get_agent():
    """컴파일된 Agent 반환

    Returns:
        컴파일된 Agent 그래프
    """
    return create_agent_graph()
