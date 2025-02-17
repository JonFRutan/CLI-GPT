#jfr
import os, sys
sys.path.append("src")
from prompt import PromptGen
from rich.console import Console
from creator import Creator
from src.commands import Commands
import meta as meta
import environment as env

class CLIGPT:
    def __init__(self):
        #Rich console
        self.console = Console()
        self.environment = env.Environment(self.console)
        self.commands = Commands(self.environment).commands
        meta.clear_screen()
        self.console.print("[cyan]Connecting to API...[/cyan]")
        #This may be skipped if an (authorized) environment is imported?
        self.ready = True
        self.key = os.getenv("OPENAI_API_KEY")
        saved = None
        if not self.key:
            saved = self.environment.authenticate()
        if self.key:
            if not self.environment.creator.validate_key(self.key):
                saved = self.environment.authenticate()
        if saved:
            self.console.print(f"[bold red]{saved}[/bold red]")
        meta.clear_screen()
        self.console.print("[bold cyan]CLI-GPT[/bold cyan]\n[bold green]Type '!exit' or hit Ctrl+C to exit the program.\nType '!help' to see more commands.[/bold green]")
    
    def run(self):
        try:
            #PromptGen should be moved under the Creator object.
            prompt = PromptGen(self.environment.file_manager)
            while True:    
                #NOTE; Look for another way to handle inputs.
                user_input = self.console.input("[bold cyan][> [/bold cyan]")
                head = user_input.split(" ")[0]
                if head in ["!exit", "exit"]:
                    self.console.print("Exiting...")
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
                    #FIXME;
                    api_prompt = prompt.generate(user_input)
                    response = self.environment.creator.generate_response(api_prompt)
                    for chunk in response:
                        buffer = chunk.choices[0].delta.content
                        if buffer:
                           self.console.print(f"[white]{buffer}[white]", end="")
                self.console.print()
        except KeyboardInterrupt:
            print("Exiting")
            exit()

if __name__ == "__main__":
    cli_gpt = CLIGPT()
    #Pre-processing stuff...
    cli_gpt.run()