"""
텍스트 청킹 모듈
"""

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import get_settings


class LawTextSplitter:
    """법률 문서 전용 텍스트 분할기"""

    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ):
        """
        Args:
            chunk_size: 청크 크기 (기본값: 설정에서 로드)
            chunk_overlap: 청크 겹침 크기 (기본값: 설정에서 로드)
        """
        settings = get_settings()
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap

        # 법률 문서에 맞는 구분자 설정
        self.separators = [
            "\n제",  # 조문이 \n제1조 형태임. 
            "\n\n",  # 문단 구분
            "\n",  # 줄바꿈
            ".",  # 문장 구분
            " ",  # 단어 구분
        ]

    def split(self, documents: List[Document]) -> List[Document]:
        """문서 분할

        Args:
            documents: 원본 문서 리스트

        Returns:
            분할된 Document 리스트
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
            length_function=len,
            keep_separator=True,
        )

        split_docs = splitter.split_documents(documents)

        # 청크 인덱스 메타데이터 추가
        for idx, doc in enumerate(split_docs):
            doc.metadata["chunk_index"] = idx

        return split_docs


def split_documents(
    documents: List[Document],
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> List[Document]:
    """문서 분할 유틸리티 함수

    Args:
        documents: 원본 문서 리스트
        chunk_size: 청크 크기
        chunk_overlap: 청크 겹침 크기

    Returns:
        분할된 Document 리스트
    """
    splitter = LawTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split(documents)
