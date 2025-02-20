#jfr
import os

from rich.console import Console
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
#from prompt_toolkit.styles import Style

from src.commands import Commands
from src.environment import Environment
from src.creator import Creator
import src.meta as meta

#NOTE; I'd like to add a few functionalities to this class:
# 1. Argument support - start the app with an argument like a settings profile import
# 2. Instance alternative to repl(), CLIGPT should serve also as an instiatble object, and forego the repl() function.
#    This would greatly improve it's ability to automate tasks.
class CLIGPT:
    #Should console exist only when running repl? 
    def __init__(self):
        #Rich console
        self.console = Console()
        self.environment = Environment(self.console)
        meta.clear_screen()
        self.history = InMemoryHistory()

        self.console.print("[cyan]Connecting to API...[/cyan]")
        #This may be skipped if an (authorized) environment is imported?
        key = os.getenv("OPENAI_API_KEY")
        saved = self.creator = Creator(self.environment, key)
        if saved:
            self.console.print(f"[bold red]{saved}[/bold red]")
        meta.clear_screen()
        self.commands = Commands(self.environment, self.creator).commands
        self.console.print("[bold cyan]CLI-GPT[/bold cyan]\n[bold green]Type '!exit' or hit Ctrl+C to exit the program.\nType '!help' to see more commands.[/bold green]")
    
    def generate(self, prompt, *args):
        pass

    def repl(self):
        if self.environment.defined_default:
            self.console.print("Default profile imported.")
        try:
            while True:    
                user_input = prompt(f">> ", history=self.history, style=meta.INPUT_STYLE)
                head = user_input.split(" ")[0]
                if head in ["!exit", "!quit"]:
                    exit()
                elif head in self.commands:
                    args = user_input.split(" ")[1:]
                    if not args:
                        result = self.commands[head].execute()
                    else:
                        #self.console.print(f"[bold blue]ARGS: {args}[/bold blue]")
                        result = self.commands[head].execute(*args)
                    if result:
                        self.console.print(f"[bright_white]{result}[/bright_white]", end="")
                else:
                    response = self.creator.generate_response(user_input)
                    for chunk in response:
                        buffer = chunk.choices[0].delta.content
                        if buffer:
                          self.console.print(f"[turquoise2]{buffer}[/turquoise2]", end="")
                
                self.console.print()
        except KeyboardInterrupt:
            exit()

if __name__ == "__main__":
    cli_gpt = CLIGPT()
    #Pre-processing stuff...
    cli_gpt.repl()