import os
import platform

OS_TYPE = platform.system()
MODEL_LIST = ["gpt-4o-mini", "gpt-4o", "gpt-3-5-turbo", "gpt-4"]

def clear_screen():
    os.system("cls" if OS_TYPE=="Windows" else "clear")

def save_environment_variable(api_key):
    if OS_TYPE in ["Linux", "Darwin"]: #POSIX systems; Linux, and Darwin for MAC
       shell = os.path.expanduser("~/.bashrc")
       if os.path.exists(os.path.expanduser("~/.zshrc")):
           shell = os.path.expanduser("~/.zshrc")
       with open(shell, "a") as console:
            console.write(f'\nexport OPENAI_API_KEY="{api_key}"\n')
            print(f"API key saved. Restart your terminal to update it.")

    elif OS_TYPE == "Windows":
        os.system(f'setx OPENAI_API_KEY "{api_key}"')

        print(f"API key saved. Restart your terminal to update it.")
    else:
        print(f"Unsupported OS: {OS_TYPE}. Try setting the env variable manually.\nCreate an issue or message me if you see this!")