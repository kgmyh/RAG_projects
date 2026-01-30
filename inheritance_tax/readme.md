python -m src.main index# 상속세 및 증여세법 RAG 기반 법률 서비스 Agent

상속세 및 증여세법에 관한 질문에 답변하는 RAG(Retrieval-Augmented Generation) 기반 AI 법률 상담 서비스입니다.

## 📋 목차

- [개요](#개요)
- [프로젝트 구조](#프로젝트-구조)
- [모듈별 역할](#모듈별-역할)
- [설치 방법](#설치-방법)
- [사용 방법](#사용-방법)
- [설정](#설정)
- [개발](#개발)

---

## 개요

이 프로젝트는 **상속세 및 증여세법(법률)(제21065호)(20260102)** 문서를 기반으로 법률 관련 질문에 답변하는 AI 서비스입니다.

### 주요 기술 스택

- **LangChain**: LLM 애플리케이션 프레임워크
- **LangGraph**: 상태 기반 Agent 워크플로우
- **Qdrant**: 벡터 데이터베이스
- **OpenAI**: 임베딩 및 LLM 모델

---

## 프로젝트 구조

```
inheritance_tax/
├── data/                           # 법률 문서 (PDF)
│   └── 상속세 및 증여세법(법률)(제21065호)(20260102).pdf
├── src/
│   ├── __init__.py
│   ├── main.py                     # CLI 진입점
│   ├── config.py                   # 설정 관리
│   │
│   ├── document/                   # 문서 처리 모듈
│   │   ├── __init__.py
│   │   ├── loader.py               # PDF 로더
│   │   ├── splitter.py             # 텍스트 청킹
│   │   └── preprocessor.py         # 전처리
│   │
│   ├── vectorstore/                # 벡터 DB 모듈
│   │   ├── __init__.py
│   │   ├── embeddings.py           # OpenAI 임베딩
│   │   ├── qdrant_store.py         # Qdrant 연결
│   │   └── indexer.py              # 인덱싱 로직
│   │
│   ├── retriever/                  # 검색 모듈
│   │   ├── __init__.py
│   │   ├── base_retriever.py       # 기본 검색기
│   │   └── hybrid_retriever.py     # 하이브리드 검색
│   │
│   ├── agent/                      # LangGraph Agent 모듈
│   │   ├── __init__.py
│   │   ├── state.py                # Agent 상태 정의
│   │   ├── nodes.py                # 그래프 노드
│   │   ├── tools.py                # Agent 도구
│   │   └── graph.py                # 워크플로우
│   │
│   ├── chain/                      # LangChain 체인 모듈
│   │   ├── __init__.py
│   │   ├── prompts.py              # 프롬프트 템플릿
│   │   └── rag_chain.py            # RAG 체인
│   │
│   └── cli/                        # CLI 인터페이스
│       ├── __init__.py
│       └── interface.py            # CLI 명령어
│
├── scripts/
│   └── index_documents.py          # 인덱싱 스크립트
│
├── tests/                          # 테스트
│   ├── __init__.py
│   ├── test_loader.py
│   ├── test_retriever.py
│   └── test_agent.py
│
├── .env.example                    # 환경변수 예시
├── .gitignore
├── pyproject.toml                  # 프로젝트 설정
├── requirements.txt                # 의존성
└── readme.md
```

---

## 모듈별 역할

### 📄 `document/` - 문서 처리

| 파일 | 역할 |
|------|------|
| `loader.py` | PDF 파일을 로드하여 LangChain Document 객체로 변환 |
| `splitter.py` | 법률 문서에 최적화된 텍스트 청킹 (조문 단위 구분) |
| `preprocessor.py` | 불필요한 문자 제거, 법률 용어 정규화 등 전처리 |

### 🗄️ `vectorstore/` - 벡터 데이터베이스

| 파일 | 역할 |
|------|------|
| `embeddings.py` | OpenAI 임베딩 모델 설정 및 인스턴스 생성 |
| `qdrant_store.py` | Qdrant 클라이언트 연결 및 벡터 스토어 관리 |
| `indexer.py` | 문서 로드 → 전처리 → 청킹 → 벡터화 → 저장 파이프라인 |

### 🔍 `retriever/` - 검색

| 파일 | 역할 |
|------|------|
| `base_retriever.py` | Qdrant 기반 유사도 검색 |
| `hybrid_retriever.py` | 벡터 + 키워드 하이브리드 검색 (확장용) |

### 🤖 `agent/` - LangGraph Agent

| 파일 | 역할 |
|------|------|
| `state.py` | Agent의 상태 스키마 정의 (TypedDict) |
| `nodes.py` | 검색, 평가, 생성 등 그래프 노드 함수 |
| `tools.py` | Agent가 사용할 도구 정의 (법률 검색, 조문 조회) |
| `graph.py` | LangGraph 워크플로우 구성 및 컴파일 |

### ⛓️ `chain/` - LangChain 체인

| 파일 | 역할 |
|------|------|
| `prompts.py` | 시스템 프롬프트, RAG 프롬프트 템플릿 |
| `rag_chain.py` | LLM과 프롬프트를 연결한 RAG 체인 구성 |

### 💻 `cli/` - CLI 인터페이스

| 파일 | 역할 |
|------|------|
| `interface.py` | 대화형 채팅 UI, 인덱싱 명령어 처리 |

---

## 설치 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd inheritance_tax
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 설치 라이브러리

| 패키지 | 버전 | 용도 |
|--------|------|------|
| `langchain` | ≥0.3.0 | LLM 애플리케이션 프레임워크 |
| `langchain-core` | ≥0.3.0 | LangChain 핵심 모듈 |
| `langchain-community` | ≥0.3.0 | 커뮤니티 통합 모듈 |
| `langchain-openai` | ≥0.2.0 | OpenAI 연동 |
| `langgraph` | ≥0.2.0 | 상태 기반 Agent 그래프 |
| `qdrant-client` | ≥1.12.0 | Qdrant 벡터 DB 클라이언트 |
| `langchain-qdrant` | ≥0.2.0 | LangChain-Qdrant 통합 |
| `pypdf` | ≥5.0.0 | PDF 파일 처리 |
| `unstructured` | ≥0.16.0 | 비정형 문서 처리 |
| `typer` | ≥0.15.0 | CLI 프레임워크 |
| `rich` | ≥13.9.0 | CLI 출력 포매팅 |
| `python-dotenv` | ≥1.0.0 | 환경변수 관리 |
| `pydantic` | ≥2.0.0 | 데이터 검증 |
| `pydantic-settings` | ≥2.0.0 | 설정 관리 |
| `pytest` | ≥8.0.0 | 테스트 프레임워크 |

### 4. 환경변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 열어 API 키 설정:

```env
OPENAI_API_KEY=your-openai-api-key-here
```

### 5. Qdrant 실행

Docker로 Qdrant 실행:

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

---

## 사용 방법

### 1. 문서 인덱싱

먼저 법률 문서를 벡터 DB에 인덱싱합니다:

```bash
# 방법 1: CLI 명령어
python -m src.main index

# 방법 2: 스크립트 직접 실행
python scripts/index_documents.py
```

### 2. 대화형 상담 시작

```bash
python -m src.main chat
```

### 3. 질문 예시

```
질문: 상속세 기본 공제액은 얼마인가요?

질문: 증여세 세율은 어떻게 되나요?

질문: 상속세 신고 기한은 언제인가요?

질문: 제14조에 대해 설명해주세요
```

### CLI 명령어

| 명령어 | 설명 |
|--------|------|
| `python -m src.main chat` | 대화형 상담 시작 |
| `python -m src.main index` | 문서 인덱싱 |
| `python -m src.main version` | 버전 정보 출력 |

---

## 설정

### 환경변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `OPENAI_API_KEY` | OpenAI API 키 | (필수) |
| `QDRANT_HOST` | Qdrant 호스트 | `localhost` |
| `QDRANT_PORT` | Qdrant 포트 | `6333` |
| `QDRANT_COLLECTION_NAME` | 컬렉션 이름 | `inheritance_tax_law` |
| `EMBEDDING_MODEL` | 임베딩 모델 | `text-embedding-3-small` |
| `LLM_MODEL` | LLM 모델 | `gpt-4o-mini` |
| `LLM_TEMPERATURE` | 응답 온도 | `0.0` |
| `CHUNK_SIZE` | 청크 크기 | `1000` |
| `CHUNK_OVERLAP` | 청크 겹침 | `200` |

---

## 개발

### 테스트 실행

```bash
pytest tests/ -v
```

### 코드 포매팅

```bash
black src/ tests/
ruff check src/ tests/
```

---

## 데이터 수집

법률 문서는 아래 링크에서 다운로드:

- https://www.law.go.kr/법령/상속세및증여세법

1. PDF로 다운로드
2. `data/` 디렉토리에 복사

---

## 라이선스

MIT License

---

## 주의사항

⚠️ 이 서비스는 법률 자문이 아닌 **정보 제공 목적**입니다.
구체적인 사안에 대해서는 전문 세무사나 변호사와 상담하시기 바랍니다.
