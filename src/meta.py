#NOTE;
# meta.py should store solely global data and perform console functions like clear screen.
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

def import_file(file_path):
    if not os.path.isfile(file_path):
        print (f"File {file_path} doesn't exist.")
        return
    file_type = file_path[::-1].split(".")[0][::-1]   #Reverses, cuts at period, slices, reverses again
    #NOTE; you can also use os.path.splitext to get the filetype, but I already made this.
    reference_name = input(f"{file_path} found. Provide a reference name: ").strip()
    IMPORTED_FILES[reference_name] = ImportedFile(reference_name, file_path, file_type)
    return

def retrieve_file(ref):
    if ref in IMPORTED_FILES:
        working_file = IMPORTED_FILES[ref]
        if working_file.type in TEXT_FILES:
            with open (working_file.path, 'r') as file:
                return file.read()
        elif working_file.type in IMAGE_FILES:  
            pass     
    else:
        print(f"Reference {ref} unknown.")

class ImportedFile:
    def __init__(self, ref, path, type):
        self.ref = ref
        self.path = path
        self.type = type
