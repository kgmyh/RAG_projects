# Rich는 터미널에 색상, 스타일, 표, 마크다운, 진행 바 등 화려한 출력을 가능하게 하는 라이브러리
# pip install rich
#  pip install "typer[all]" # typer와 rich를 함께 설치
# Typer로 명령어, 인수(argument), 옵션(option) 정의.
# Rich로 print 함수를 대체하여 색상과 구조가 포함된 결과 출력.
# Rich의 Table을 사용하여 데이터를 체계적으로 표현. 

from rich.console import Console
from rich.panel import Panel


console = Console()

panel = Panel("Hello, Rich!", style="bold magenta")
console.print(panel)

console.print("밑줄 + 글자 굵게 빨갛게 출력!", style="bold underline red") # 순서상관없다. 
console.print("가운데 정렬", justify="left", style="bold")
console.print("왼쪽 정렬", justify="center", style="bold")
console.print("오른쪽 정렬", justify="right", style="bold")


from rich import print # 단순 프린트
print("Hello, [bold magenta]World[/bold magenta]!", # 태그로 font-weight, color 지정
       ":vampire:", # 이모지 출력 
       locals()) # 로컬 변수 출력 key-value 색을 다르게 출력해줌

# onsole.print 함수를 사용하면, rich 모듈이 지원하는 다양한 스타일 옵션을 활용하여 텍스트를 출력할 수 있습니다. 예를 들어, style 옵션을 사용하여 텍스트의 색깔, 굵기, 밑줄 등을 조절할 수 있습니다. 또한 justify 옵션을 사용하여 텍스트를 가운데, 왼쪽, 오른쪽으로 정렬할 수 있습니다.
