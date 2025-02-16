#jfr
import os, sys
sys.path.append("src")
from prompt import Prompt
from rich.console import Console
from creator import Creator
from src.commands import Commands
import meta as meta

meta.clear_screen()

console = Console()
console.print("[cyan]Connecting to API...[/cyan]")

#FIXME; the user object should have persistent data, so if the system is highly tailored it will be saved.
#Creating a basic client
user_creator = Creator("gpt-4o-mini", "Be a bit brief. When formatting text avoid markdown and use plain text.", None)

ready = True
key = os.getenv("OPENAI_API_KEY")
if key:
    user_creator.validate_key(key)
    if not user_creator.ai_client:
        ready = False
if not key:
    ready = False

meta.clear_screen()

#This loop executes if the local environment key either doesn't exist, or doesn't work.
while not ready:
    api_key = input("Please provide your OpenAI API key (? for help, x for exit.): ")
    if api_key == "?":
        console.print("Navigate to platform.openai.com, sign in, under PROJECT is an API key section.")
    elif api_key == 'x':
        console.print("Exiting...")
        exit()
    else:
        user_creator.validate_key(api_key)
        if user_creator.ai_client:
            ready = True
            save = input("Would you like to save the key to your system environment? (y/n)")
            if save.lower() == 'y':
                meta.save_environment_variable(api_key)
meta.clear_screen()

commands_init = Commands(user_creator)
commands = commands_init.commands
console.print("[bold cyan]CLI-GPT[/bold cyan]\n[bold green]Type '!exit' or hit Ctrl+C to exit the program.\nType '!help' to see more commands.[/bold green]")

try:
    while True:    
        user_input = console.input("[bold cyan][> [/bold cyan]")
        head = user_input.split(" ")[0]
        if user_input in ["!exit", "exit"]:
            console.print("Exiting...")
            exit()

        elif head in commands:
            args = user_input.split(" ")[1:]
            if not args:
                result = commands[head].execute()
            else:
                console.print(f"[bold blue]ARGS: {args}[/bold blue]")
                result = commands[head].execute(*args)
            if result:
                console.print(f"[bold green]{result}[/bold green]", end="")

        else:
            sys_prompt = Prompt(user_input)
            response = user_creator.generate_response(sys_prompt.body)
            for chunk in response:
                buffer = chunk.choices[0].delta.content
                if buffer:
                    console.print(buffer, end="")
        console.print()
except KeyboardInterrupt:
    print("Exiting")
    exit()


#if __name__ == "__main__":
#    main()