"""
Qdrant 벡터 스토어 모듈
"""

from typing import List, Optional

from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from src.config import get_settings
from src.vectorstore.embeddings import get_embeddings


def get_qdrant_client() -> QdrantClient:
    """Qdrant 클라이언트 인스턴스 반환

    Returns:
        QdrantClient 인스턴스
    """
    settings = get_settings()

    return QdrantClient(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
    )


class QdrantStore:
    """Qdrant 벡터 스토어 관리 클래스"""

    def __init__(
        self,
        collection_name: Optional[str] = None,
        client: Optional[QdrantClient] = None,
    ):
        """
        Args:
            collection_name: 컬렉션 이름
            client: Qdrant 클라이언트 (없으면 새로 생성)
        """
        settings = get_settings()
        self.collection_name = collection_name or settings.qdrant_collection_name
        self.client = client or get_qdrant_client()
        self.embeddings = get_embeddings()

    def create_collection(self, vector_size: int = 1536) -> None:
        """컬렉션 생성

        Args:
            vector_size: 벡터 차원 (text-embedding-3-small: 1536)
        """
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]

        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def delete_collection(self) -> None:
        """컬렉션 삭제"""
        self.client.delete_collection(collection_name=self.collection_name)

    def add_documents(self, documents: List[Document]) -> None:
        """문서 추가

        Args:
            documents: 추가할 문서 리스트
        """
        vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings,
        )
        vector_store.add_documents(documents)

    def get_vector_store(self) -> QdrantVectorStore:
        """벡터 스토어 인스턴스 반환

        Returns:
            QdrantVectorStore 인스턴스
        """
        return QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings,
        )
