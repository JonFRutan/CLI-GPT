#jfr
import os

from rich.console import Console
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style

from src.commands import Commands
from src.environment import Environment
from src.creator import Creator
import src.meta as meta


class CLIGPT:
    def __init__(self):
        #Rich console
        self.console = Console()
        self.environment = Environment(self.console)
        self.creator = Creator(self.environment.prompt_config, self.environment.file_manager)
        self.commands = Commands(self.environment, self.creator).commands
        meta.clear_screen()
        self.history = InMemoryHistory()

        self.console.print("[cyan]Connecting to API...[/cyan]")
        #This may be skipped if an (authorized) environment is imported?
        key = os.getenv("OPENAI_API_KEY")
        saved = None
        if not key or not self.creator.validate_key(key):
            saved = self.creator.authenticate()
            if saved:
                self.console.print(f"[bold red]{saved}[/bold red]")
        meta.clear_screen()
        self.console.print("[bold cyan]CLI-GPT[/bold cyan]\n[bold green]Type '!exit' or hit Ctrl+C to exit the program.\nType '!help' to see more commands.[/bold green]")
    
    def run(self):
        input_style = Style.from_dict({
            'prompt': 'bold cyan'
        })
        try:
            while True:    
                user_input = prompt(f">> ", history=self.history, style=input_style)
                head = user_input.split(" ")[0]
                if head in ["!exit", "exit"]:
                    exit()
                elif head in self.commands:
                    args = user_input.split(" ")[1:]
                    if not args:
                        result = self.commands[head].execute()
                    else:
                        self.console.print(f"[bold blue]ARGS: {args}[/bold blue]")
                        result = self.commands[head].execute(*args)
                    if result:
                        self.console.print(f"[bold green]{result}[/bold green]", end="")
                else:
                    response = self.creator.generate_response(user_input)
                    for chunk in response:
                        buffer = chunk.choices[0].delta.content
                        if buffer:
                          self.console.print(f"[bright_white]{buffer}[/bright_white]", end="")
                self.console.print()
        except KeyboardInterrupt:
            exit()

if __name__ == "__main__":
    cli_gpt = CLIGPT()
    #Pre-processing stuff...
    cli_gpt.run()