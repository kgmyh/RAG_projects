#!/usr/bin/env python
"""
문서 인덱싱 스크립트
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from rich.console import Console

from src.vectorstore import index_documents

# 환경변수 로드
load_dotenv()

console = Console()


def main():
    """메인 함수"""
    console.print("[bold blue]상속세 및 증여세법 문서 인덱싱[/bold blue]\n")

    try:
        # 인덱싱 실행
        chunk_count = index_documents(recreate=True)
        console.print(f"\n[bold green]✅ 완료![/bold green] {chunk_count}개 청크가 인덱싱되었습니다.")

    except FileNotFoundError as e:
        console.print(f"[bold red]❌ 파일을 찾을 수 없습니다:[/bold red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ 오류 발생:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
