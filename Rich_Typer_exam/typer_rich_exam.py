import typer
from rich import print

def main(name: str = "World"):
    print(f"Hello [bold white on blue]{name}[/] :sparkles:") # name cli argument

if __name__ == "__main__":
    typer.run(main)