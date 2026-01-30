"""
문서 전처리 모듈
"""

import re
from typing import List

from langchain_core.documents import Document


class LawPreprocessor:
    """법률 문서 전처리기"""

    def __init__(self):
        # 법률 용어 정규화 패턴
        self.patterns = [
            # 머리글 제거
            (r"상속세 및 증여세법\n", "\n"),
            # 바닥글 페이지 번호 제거
            (r"법제처\s+\d+\s+국가법령정보센터", ""),
            # 연속된 줄바꿈 정리
            # 불필요한 공백 제거
            (r"' '+", " "),
            (r"\n{3,}", "\n\n"),
        ]

    def preprocess(self, text: str) -> str:
        """텍스트(개별 문서) 전처리 메소드

        Args:
            text: 원본 텍스트

        Returns:
            전처리된 텍스트
        """
        result = text

        for pattern, replacement in self.patterns:
            result = re.sub(pattern, replacement, result)

        return result.strip()

    def preprocess_documents(self, documents: List[Document]) -> List[Document]:
        """문서 리스트 전처리 메소드

        Args:
            documents: 원본 문서 리스트

        Returns:
            전처리된 Document 리스트
        """
        processed_docs = []

        for doc in documents:
            processed_content = self.preprocess(doc.page_content)

            # 빈 문서 제외
            if processed_content:
                processed_doc = Document(
                    page_content=processed_content,
                    metadata=doc.metadata.copy(),
                )
                processed_docs.append(processed_doc)

        return processed_docs


def preprocess_text(text: str) -> str:
    """텍스트 전처리 유틸리티 함수

    Args:
        text: 원본 텍스트

    Returns:
        전처리된 텍스트
    """
    preprocessor = LawPreprocessor()
    return preprocessor.preprocess(text)
