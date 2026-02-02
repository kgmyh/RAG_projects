from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()
console.print(Panel("Enter the file name for your memo", 
                     title="File Name", 
                     border_style="blue"))
while True:
    file_name = Prompt.ask("Enter the [bold blue]file name[/] to memo")
    confirm = Confirm.ask(f"Do you want to create or edit the file [bold red]{file_name}[/]?")
    if confirm:
        break

console.print(Panel("Type your memo content. Press Enter on empty line to finish.", 
                     title="Memo Editor", 
                     border_style="green"))
lines = []
while True:
    line = console.input(">>> ")
    if not line:  # 빈 줄 입력 시 종료
        break
    lines.append(line)