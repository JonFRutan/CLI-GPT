#NOTE;
# meta.py should store global data, perform modifications outside the environment, 
# and perform console functions like clear screen.
import os, platform

#Global, final values
OS_TYPE = platform.system()                                           #Current OS
API_MODELS_LIST = ["gpt-4o-mini", "gpt-4o", "gpt-3-5-turbo", "gpt-4"] #Available models                                       
VAR_REGEX = r"\{([a-zA-Z0-9]+)\}"                                     #For finding references

#IMAGE_FILES must be convertible into base64
IMAGE_FILES = [
    "png", 
    "jpg", "jpeg", 
    "gif", 
    "webp", 
    "bmp", 
    "tiff",
]

#TEXT_FILES must be readable and transcribable line-by-line
TEXT_FILES = [
    "txt",
    "md", 
    "html", "htm", 
    "json", 
    "py", 
    "c", "cpp", "h", 
    "xml", 
    "java", 
    "js", "ts", 
    "sql", 
    "sh", 
    "bash", 
    "yaml", "yml",
]

def clear_screen():
    os.system("cls" if OS_TYPE=="Windows" else "clear")

#Establishes a persistent API key presence.
#FIXME; there should be an option to change your API key, or at least remove it.
def save_environment_variable(api_key):
    if OS_TYPE in ["Linux", "Darwin", "FreeBSD"]: #POSIX systems; Linux, and Darwin for MAC
       shell = os.path.expanduser("~/.bashrc")
       if os.path.exists(os.path.expanduser("~/.zshrc")):
           shell = os.path.expanduser("~/.zshrc")
       with open(shell, "a") as console:
            console.write(f'\nexport OPENAI_API_KEY="{api_key}"\n')
            print(f"API key saved. Restart your terminal to update it.")
    elif OS_TYPE == "Windows":
        os.system(f'setx OPENAI_API_KEY "{api_key}"')
        return "API key saved. Restart your terminal to update it."
    else:
        print(f"Unsupported OS: {OS_TYPE}. Try setting the env variable manually.\nCreate an issue or message me if you see this!")