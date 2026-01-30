from rich.console import Console
from rich.panel import Panel
import time
console = Console()

# 기본 패널 사용
console.print(Panel("안녕하세요! Rich 패널입니다."))

# 제목, 스타일, 테두리 박스 스타일 지정
with console.status("패널 생성 중..."): # 출력전까지 status 문자열이 출력된다.
    time.sleep(1)  # 작업 시뮬레이션
    panel = Panel(
        "여기에 중요한 내용이 들어갑니다.",
        title="[bold blue]알림[/bold blue]",
        subtitle="2024-05",
        style="white on blue",
        border_style="red",
        expand=False  # 전체 너비
    )
    console.print(panel)
