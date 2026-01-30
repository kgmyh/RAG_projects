"""
CLI 인터페이스 모듈
"""

import typer
from rich.console import Console
from rich.panel import Panel # 패키지에서 Panel(패널)은 터미널 출력 화면에서 텍스트나 다른 컨텐츠(테이블, 마크다운 등) 주위에 테두리(Border)를 그려 시각적으로 구조화하고 강조하는 역할
from rich.markdown import Markdown
from rich.prompt import Prompt # 입력 받기(input 역할) https://rich.readthedocs.io/en/latest/prompt.html

from src.agent import get_agent
from src.vectorstore import index_documents

console = Console()


def print_welcome():
    """환영 메시지 출력"""
    welcome_text = """
# 🏛️ 상속세 및 증여세법 AI 상담 서비스

상속세 및 증여세법에 관한 질문을 입력해주세요.

**명령어:**
- `exit` 또는 `quit`: 프로그램 종료
- `clear`: 대화 기록 초기화
- `help`: 도움말 표시

---
"""
    console.print(Markdown(welcome_text))


def print_help():
    """도움말 출력"""
    help_text = """
## 도움말

### 질문 예시
- "상속세 기본 공제액은 얼마인가요?"
- "증여세 세율은 어떻게 되나요?"
- "상속세 신고 기한은 언제인가요?"
- "제14조에 대해 설명해주세요"

### 명령어
- `exit`, `quit`: 프로그램 종료
- `clear`: 대화 기록 초기화
- `help`: 이 도움말 표시
"""
    console.print(Markdown(help_text))


def run_chat():
    """대화형 채팅 실행"""
    print_welcome()

    agent = get_agent()

    while True:
        try:
            # 사용자 입력
            user_input = Prompt.ask("\n[bold blue]질문[/bold blue]")

            if not user_input.strip():
                continue

            # 명령어 처리
            if user_input.lower() in ["exit", "quit", "종료"]:
                console.print("\n[yellow]프로그램을 종료합니다. 감사합니다![/yellow]")
                break

            if user_input.lower() == "clear":
                console.clear()
                print_welcome()
                continue

            if user_input.lower() == "help":
                print_help()
                continue

            # Agent 실행
            ## 
            with console.status("[bold green]답변 생성 중...[/bold green]"):
                result = agent.invoke({
                    "question": user_input,
                    "messages": [],
                    "documents": [],
                    "answer": None,
                    "relevance_score": None,
                    "needs_more_search": False,
                })

            # 검색된 문서(Context) 출력
            documents = result.get("documents", [])
            if documents:
                context_text = ""
                for i, doc in enumerate(documents, 1):
                    source = doc.metadata.get("source", "알 수 없음")
                    page = doc.metadata.get("page", "")
                    page_info = f" (p.{page})" if page else ""
                    context_text += f"**[{i}] {source}{page_info}**\n"
                    # 문서 내용 미리보기 (최대 300자)
                    content_preview = doc.page_content[:300]
                    if len(doc.page_content) > 300:
                        content_preview += "..."
                    context_text += f"{content_preview}\n\n"
                
                console.print(Panel(
                    Markdown(context_text),
                    title=f"[bold cyan]📚 검색된 문서 ({len(documents)}건)[/bold cyan]",
                    border_style="cyan",
                ))

            # 답변 출력
            answer = result.get("answer", "답변을 생성할 수 없습니다.")
            console.print(Panel(
                Markdown(answer),
                title="[bold green]답변[/bold green]",
                border_style="green",
            ))

        except KeyboardInterrupt:
            console.print("\n[yellow]프로그램을 종료합니다.[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]오류가 발생했습니다: {e}[/red]")


def index_documents_cli():
    """문서 인덱싱 CLI"""
    console.print(Panel(
        "문서 인덱싱을 시작합니다.",
        title="[bold blue]인덱싱[/bold blue]",
        border_style="blue",
    ))

    try:
        recreate = typer.confirm("기존 인덱스를 삭제하고 재생성하시겠습니까?", default=False)
        chunk_count = index_documents(recreate=recreate)

        console.print(Panel(
            f"✅ 인덱싱 완료: {chunk_count}개 청크가 저장되었습니다.",
            title="[bold green]완료[/bold green]",
            border_style="green",
        ))
    except Exception as e:
        console.print(Panel(
            f"❌ 인덱싱 실패: {e}",
            title="[bold red]오류[/bold red]",
            border_style="red",
        ))
