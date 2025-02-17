#NOTE;
# meta.py should store global data, perform modifications outside the environment, 
# and perform console functions like clear screen.
import os, platform

OS_TYPE = platform.system()                                      #Current OS
MODEL_LIST = ["gpt-4o-mini", "gpt-4o", "gpt-3-5-turbo", "gpt-4"] #Available models
IMPORTED_FILES = {}                                              #Dictionary for files                                              
VAR_REGEX = r"\{([a-zA-Z0-9]+)\}"                                #For finding references

# FIXME; This is rudimentary and early categorizations of the types of files that can be uploaded.
# Anything that can be read in line-by-line should be under TEXT_FILES
# Image file types should be under IMAGE_FILES
# For now, only select file types will be strictly defined...
IMAGE_FILES = ["png", "jpg", "gif", "webp"]
TEXT_FILES = ["txt", "doc", "md", "html", "json", "py", "c", "xml"]

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

        print(f"API key saved. Restart your terminal to update it.")
    else:
        print(f"Unsupported OS: {OS_TYPE}. Try setting the env variable manually.\nCreate an issue or message me if you see this!")