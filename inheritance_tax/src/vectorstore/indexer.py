"""
문서 인덱싱 모듈
"""

from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.config import get_settings
from src.document import load_pdf_documents, split_documents, LawPreprocessor
from src.vectorstore.qdrant_store import QdrantStore

console = Console()


class DocumentIndexer:
    """문서 인덱싱 클래스"""

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Args:
            data_dir: 데이터 디렉토리 경로
        """
        settings = get_settings()
        self.data_dir = data_dir or settings.data_dir
        self.qdrant_store = QdrantStore()
        self.preprocessor = LawPreprocessor()

    def index(self, recreate: bool = False) -> int:
        """문서 인덱싱 실행

        Args:
            recreate: 기존 컬렉션 삭제 후 재생성 여부

        Returns:
            인덱싱된 문서 수
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # 1. 컬렉션 준비
            progress.add_task(description="컬렉션 준비 중...", total=None)
            if recreate:
                try:
                    self.qdrant_store.delete_collection()
                except Exception:
                    pass
            self.qdrant_store.create_collection()

            # 2. PDF 문서 로드
            task = progress.add_task(description="PDF 문서 로드 중...", total=None)
            documents = load_pdf_documents(self.data_dir)
            progress.update(task, description=f"PDF 문서 {len(documents)}개 로드 완료")

            # 3. 전처리
            task = progress.add_task(description="문서 전처리 중...", total=None)
            documents = self.preprocessor.preprocess_documents(documents)
            progress.update(task, description=f"전처리 완료: {len(documents)}개 문서")

            # 4. 텍스트 분할
            task = progress.add_task(description="텍스트 분할 중...", total=None)
            chunks = split_documents(documents)
            progress.update(task, description=f"텍스트 분할 완료: {len(chunks)}개 청크")

            # 5. 벡터 DB에 저장
            task = progress.add_task(description="벡터 DB에 저장 중...", total=None)
            self.qdrant_store.add_documents(chunks)
            progress.update(task, description=f"벡터 DB 저장 완료: {len(chunks)}개 청크")

        return len(chunks)


def index_documents(data_dir: Optional[Path] = None, recreate: bool = False) -> int:
    """문서 인덱싱 유틸리티 함수

    Args:
        data_dir: 데이터 디렉토리 경로
        recreate: 기존 컬렉션 삭제 후 재생성 여부

    Returns:
        인덱싱된 문서 수
    """
    indexer = DocumentIndexer(data_dir=data_dir)
    return indexer.index(recreate=recreate)
