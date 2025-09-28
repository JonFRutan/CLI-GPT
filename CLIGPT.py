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
        if not args:
            self.environment.prompt_config.stream = False
            response = self.creator.generate_response(prompt)
            return response.output_text
        #FIXME - This command splitter doesn't work.
        results = []
        current = None
        for item in args[0]:
            if item in self.commands:
                if current:
                    results.append(tuple(current))
                current = [item]
            else:
                if current:
                    current.append(item)
        if current:
            results.append(tuple(current))
        return results #FIXME

    #FIXME: This is broken
    def grab_args(self, user_arguments):
        args = []
        recent_word = 0
        sub_index = 0
        for i, char in enumerate(user_arguments):
            if char == " ":
                args.append(f"{user_arguments[recent_word:i]}")
                recent_word = i
            if char == '"':
                for k, subchar in enumerate(user_arguments[i+1:]):
                    if subchar == '"':
                        #print(i)
                        #print(recent_word)
                        #print(k)
                        args.append(f"{user_arguments[i:i+k+2]}")
                        slice1 = user_arguments[:i-1]
                        slice2 = user_arguments[i+k+2:]
                        print(slice1)
                        print(slice2)
                        user_arguments = slice1+slice2
                        break
        return args

        """
        args = user_arguments.split(" ")
        for i, arg in enumerate(args):
            print(arg)
            if arg[0] == '"':
               print("first branch hit")
               for j, subarg in enumerate(args[i+1:]):
                   print(f"SUBARG: {subarg}")
                   if subarg[-1] == '"':
                        print("second branch hit")
                        args[i] = f"{args[i:j]}"
                        del args[i+1:j]
                        break
        return args
        """
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
                if head in ["!exit", "!quit", "exit", "quit"]:
                    exit()
                #FIXME; This should branch if the first character in the input is an '!'
                elif head in self.commands:
                    #FIXME: If a string is provided it splits the string into multiple arguments.
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
                    if response is None:
                        print("Error generating response")
                    for chunk in response:
                        buffer = ""
                        if chunk.type == "response.output_text.delta":
                            buffer = chunk.delta
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