"""
프롬프트 템플릿 모듈
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


SYSTEM_PROMPT = """당신은 상속세 및 증여세법 전문 법률 상담 AI 어시스턴트입니다.

## 역할
- 상속세 및 증여세법에 관한 질문에 정확하고 전문적인 답변을 제공합니다.
- 제공된 법률 문서 컨텍스트를 기반으로 답변합니다.
- 법률 용어를 쉽게 설명하고, 필요시 관련 조문을 인용합니다.

## 답변 지침
1. 항상 제공된 컨텍스트를 기반으로 답변하세요.
2. 컨텍스트에 없는 내용은 "제공된 자료에서 확인할 수 없습니다"라고 답변하세요.
3. 관련 조문이 있으면 조문 번호와 함께 인용하세요.
4. 복잡한 법률 개념은 일반인도 이해할 수 있도록 쉽게 설명하세요.
5. 세금 계산이 필요한 경우, 계산 과정을 단계별로 설명하세요.

## 주의사항
- 이 답변은 법률 자문이 아닌 정보 제공 목적입니다.
- 구체적인 사안에 대해서는 전문 세무사나 변호사 상담을 권장하세요.
- 법률은 개정될 수 있으므로, 최신 법령을 확인하도록 안내하세요.
"""


RAG_PROMPT_TEMPLATE = """다음 컨텍스트를 참고하여 질문에 답변하세요.

## 컨텍스트
{context}

## 질문
{question}

## 답변
"""


def get_system_prompt() -> str:
    """시스템 프롬프트 반환

    Returns:
        시스템 프롬프트 문자열
    """
    return SYSTEM_PROMPT


def get_rag_prompt() -> ChatPromptTemplate:
    """RAG 프롬프트 템플릿 반환

    Returns:
        ChatPromptTemplate 인스턴스
    """
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", RAG_PROMPT_TEMPLATE),
    ])


def get_chat_prompt() -> ChatPromptTemplate:
    """대화형 프롬프트 템플릿 반환

    Returns:
        ChatPromptTemplate 인스턴스
    """
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", RAG_PROMPT_TEMPLATE),
    ])
