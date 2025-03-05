#jfr
import os, sys

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
class CLIGPT:
    #Should console exist only when running repl? 
    def __init__(self, *args, **kwargs):
        #Rich console
        self.console = Console()
        self.environment = Environment(self.console)
        key = os.getenv("OPENAI_API_KEY")
        saved = self.creator = Creator(self.environment, key)
        self.commands = Commands(self.environment, self.creator).commands #could also be in repl
        #if saved:
        #    self.console.print(f"[bold red]{saved}[/bold red]")

    def generate(self, prompt, *args):
        #args should unroll several command calls.
        #Example: if arg[2] in self.commands: self.commands[head].execute
        #Issue here is when delimit subarguments.
        self.environment.prompt_config.stream = False
        response = self.creator.generate_response(prompt)
        return response.choices[0].message.content

    def repl(self):
        message_history = InMemoryHistory()
        meta.clear_screen()
        self.console.print("[bold cyan]CLI-GPT[/bold cyan]\n[bold green]Type '!exit' or hit Ctrl+C to exit the program.\nType '!help' to see more commands.[/bold green]")
        if self.environment.defined_default:
            self.console.print("Default profile imported.")
        try:
            while True:    
                user_input = prompt(f">> ", history=message_history, style=meta.INPUT_STYLE)
                head = user_input.split(" ")[0]
                if head in ["!exit", "!quit"]:
                    exit()
                #FIXME; This should branch if the first character in the input is an '!'
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
    args = sys.argv[1:]
    cli_gpt = CLIGPT()
    if not args:
        cli_gpt.repl()
    else:
        print(cli_gpt.generate(*args))