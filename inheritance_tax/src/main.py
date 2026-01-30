"""
CLI 애플리케이션 진입점
"""

import typer
from dotenv import load_dotenv

from src.cli.interface import run_chat, index_documents_cli

# 환경변수 로드
load_dotenv()

app = typer.Typer(
    name="tax-agent",
    help="상속세 및 증여세법 RAG 기반 법률 서비스 Agent",
    add_completion=False,
)


@app.command()
def chat():
    """대화형 법률 상담 시작"""
    run_chat()


@app.command()
def index():
    """문서 인덱싱 실행"""
    index_documents_cli()


@app.command()
def version():
    """버전 정보 출력"""
    from src import __version__

    typer.echo(f"상속세 법률 Agent v{__version__}")


if __name__ == "__main__":
    app()
