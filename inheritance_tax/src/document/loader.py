"""
PDF 문서 로더 모듈
"""

from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader


class PDFLoader:
    """PDF 문서 로더"""

    def __init__(self, file_path: str | Path):
        """
        Args:
            file_path: PDF 파일 경로
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

    def load(self) -> List[Document]:
        """PDF 문서 로드

        Returns:
            Document 리스트
        """
        loader = PyPDFLoader(str(self.file_path))
        documents = loader.load()

        # 메타데이터 추가
        for doc in documents:
            doc.metadata["source"] = self.file_path.name
            doc.metadata["file_type"] = "pdf"

        return documents


def load_pdf_documents(data_dir: str | Path) -> List[Document]:
    """디렉토리 내 모든 PDF 문서 로드

    Args:
        data_dir: 데이터 디렉토리 경로

    Returns:
        Document 리스트
    """
    data_path = Path(data_dir)
    all_documents = []

    for pdf_file in data_path.glob("*.pdf"):
        loader = PDFLoader(pdf_file)
        documents = loader.load()
        all_documents.extend(documents)

    return all_documents
