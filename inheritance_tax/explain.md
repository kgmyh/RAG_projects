# 데이터 수집

- https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EC%83%81%EC%86%8D%EC%84%B8%EB%B0%8F%EC%A6%9D%EC%97%AC%EC%84%B8%EB%B2%95
    - PDF로 다운로드
    - data/ 로 복사


# 프롬프트
```markdown
- RAG기반의 법률 서비스 Agent를 개발하려고 한다.
- Context 문서
    - `data/` 디렉토리 아래 `상속세 및 증여세법(법률)(제21065호)(20260102)` 를 context로 서비스 한다.  
- 사용 라이브러리
    - langchain 1.0+
    - langgraph 1.0+
    - qdrant vector database
    - langchain-openai
- CLI 기반으로 서비스 할 예정이다. (GUI는 다음 버전에서 지원)

- 필요한 모듈과 패키지 구조를 추천해줘.

```