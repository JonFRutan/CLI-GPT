#jfr
import os, sys
from rich.console import Console
from system import SystemSettings
from src.commands import Commands
import meta as meta
sys.path.append("src")

console = Console()
meta.clear_screen()
console.print("[cyan]Connecting to API...[/cyan]")

#FIXME; the user object should have persistent data, so if the system is highly tailored it will be saved.
#Creating a basic client
user = SystemSettings("gpt-4o-mini", "Be a bit brief. When formatting text avoid markdown and use plain text.", None)

ready = True
key = os.getenv("OPENAI_API_KEY")
if key:
    user.validate_key(key)
    if not user.ai_client:
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
        user.validate_key(api_key)
        if user.ai_client:
            ready = True
            save = input("Would you like to save the key to your system environment? (y/n)")
            if save.lower() == 'y':
                meta.save_environment_variable(api_key)
meta.clear_screen()

commands_init = Commands(user)
commands = commands_init.commands
console.print("[bold cyan]CLI-GPT[/bold cyan]\nType '!exit' or hit Ctrl+C to exit the program.\nType '!help' to see more commands.\n")

try:
    while True:    
        prompt = console.input("[bold cyan]> [/bold cyan]")

        if prompt in ["!exit", "exit"]:
            console.print("Exiting...")
            exit()

        elif prompt in commands:
            result = commands[prompt].execute()
            if result:
                console.print(f"[green]{result}[green]")

        else:
            response = user.generate_response(prompt)
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