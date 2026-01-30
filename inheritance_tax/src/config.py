"""
애플리케이션 설정 관리 모듈
"""

from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field

# .env 파일(config 내부클래스) 에서 설정을 로드하여 Settings 객체로 관리
class Settings(BaseSettings):
    """애플리케이션 설정"""

    # OpenAI 설정
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")

    # Qdrant 설정
    qdrant_host: str = Field(default="localhost", env="QDRANT_HOST")
    qdrant_port: int = Field(default=6333, env="QDRANT_PORT")
    qdrant_collection_name: str = Field(
        default="inheritance_tax_law", env="QDRANT_COLLECTION_NAME"
    )

    # 모델 설정
    embedding_model: str = Field(
        default="text-embedding-3-small", env="EMBEDDING_MODEL"
    )
    llm_model: str = Field(default="gpt-4o-mini", env="LLM_MODEL")
    llm_temperature: float = Field(default=0.0, env="LLM_TEMPERATURE")

    # 청킹 설정
    chunk_size: int = Field(default=1000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, env="CHUNK_OVERLAP")

    # 경로 설정
    base_dir: Path = Path(__file__).parent.parent
    data_dir: Path = base_dir / "data"

    # 객체 생성시 .env 파일을 읽어서 각 property에 매핑한다.
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # .env 파일의 추가 필드 무시 (LangSmith 등)


def get_settings() -> Settings:
    """설정 인스턴스 반환"""
    return Settings()
