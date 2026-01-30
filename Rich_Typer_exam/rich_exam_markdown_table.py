from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table


console = Console()


def print_markdown(md_text: str) -> None:
    """Markdown 문자열을 Rich로 출력"""
    console.print(Markdown(md_text))


def print_table(title: str, columns: list[str], rows: list[list[str]]) -> None:
    """테이블 출력"""
    table = Table(title=title)
    for col in columns:
        table.add_column(col) # 컬럼 추가

    for row in rows: # 행의 값 추가
        table.add_row(*[str(cell) for cell in row])
    table.add_row("A", "B", "C")
    console.print(table)


def main() -> None:
    md = """
# Rich Markdown 출력
- **굵게**
- *기울임*
- `코드`

> 인용문
"""
    print_markdown(md)

    columns = ["이름", "역할", "점수"]
    rows = [
        ["홍길동", "개발자", 95],
        ["김철수", "디자이너", 88],
        ["이영희", "기획자", 90],
    ]
    print_table("팀 정보", columns, rows)


if __name__ == "__main__":
    main()