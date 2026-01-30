# app을 이용해서 여러 명령어 등록

import typer

app = typer.Typer()
# 기본값 없음 → Argument (필수 인자)
# 기본값 있음 → Option (선택 옵션)
@app.command()
def hello(name: str): # default 없음
    print(f"Hello {name}")

@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye, Mr./Ms. {name}. It was a pleasure.")
    else:
        print(f"See you later, {name}!")

if __name__ == "__main__":
    app()