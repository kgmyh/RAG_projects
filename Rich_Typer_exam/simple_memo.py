from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()
while True:
    file_name = Prompt.ask("Enter the [bold blue]file name[/] to memo")
    confirm = Confirm.ask(f"Do you want to create or edit the file [bold red]{file_name}[/]?")
    if confirm:
        break

console.print("You can start writing your memo. Type 'exit' to finish.", style="bold green")
lines = []
while True:
    line = Prompt.ask(">>>")
    if not line:  # 빈 줄 입력 시 종료
        break
    lines.append(line)
