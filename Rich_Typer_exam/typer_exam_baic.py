# pip install typer
# --help 자동 생성

import typer

# python typer_exam_basic.py --name 홍길동
# 기본값 없음 → Argument (필수 인자)
# 기본값 있음 → Option (선택 옵션)
# 인자는 그냥 값으로 넘기고 옵션은 `--옵션명(변수)` 값 으로 넘긴다.


# 옵션	설명
# --install-completion	현재 셸에 자동완성 스크립트 설치
# --show-completion	자동완성 스크립트 내용 출력 (설치 안함)
# bash, zsh, fish, powershell 지원

def main(name: str = "World"):
    print(f"Hello {name}") # name cli argument

if __name__ == "__main__":
    typer.run(main)