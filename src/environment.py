import src.file_manager as filem
import src.meta as meta

from prompt_toolkit import prompt
from dataclasses import dataclass

import json
# The goal of environment.py is to encapsulate both API settings (tokens, system prompt, temp, etc) and the user's client settings (disabling welcome message, enabling persistent file imports, etc.) into one settings object.
# JSON will be used for settings storage, as it's easily maintainable and a user may edit it manually if need be.

class Environment:
    def __init__(self, console, *args):
        self.console = console
        self.user_settings = None
        self.prompt_config = None
        self.file_manager = filem.FileManager()
        self.defined_default = meta.check_for_default()
        if self.defined_default:
            with open(f"{self.defined_default}", "r") as file:
                json_data = json.load(file)
                self.prompt_config = PromptProfile.to_class(json_data)
        else:
            self.prompt_config = PromptProfile()

    def print_settings(self):
        return (f"Model: {self.prompt_config.model}\nSystem Prompt: {self.prompt_config.sys_prompt}")
    
    def import_profile(self, name):
        dest = f"src/profiles/{name}.json"
        try:
            with open(f"{dest}", "r") as file:
                json_data = json.load(file)
                self.prompt_config = PromptProfile.to_class(json_data)
                return f"Profile at {dest} imported."
        except Exception as e:
            return "Error importing, check profile name."
        
    def export_profile(self, name):
        return self.file_manager.export_file(self.prompt_config.jsonify(), name+".json", "src/profiles/")

    def update_settings(self, *args):
        if not args:
            meta.clear_screen()
            self.console.print("[bold underline dark_red]Settings[/bold underline dark_red]\n[red]Select a menu:\nProgram settings (u)\nPrompt settings (p)[/red]")
            response = prompt(f">> ", style=meta.INPUT_STYLE).lower()
            if response == "u":
                return self.user_settings.update_settings(self.console)
            elif response == "p":
                return self.prompt_config.update_settings(self.console)
        else:
            #self.console.print(args)
            return self.prompt_config.update_settings(self.console, args[0])



#No user settings are currently implemented
#Color scheme, Welcome message, screen clearing...
class UserSettings:
    def __init__(self):
        pass
    def update_settings(self, console):
        return "WIP"

#NOTE; It may be better to define a PromptParameter object and store the name, value, value type, and ranges.
@dataclass
class PromptProfile:

    background: bool = False
    #conversation: object = None
    input: str = ""
    instructions: str = "Be brief."
    max_output_tokens: int = 200
    max_tool_calls: int = None
    metadata: map = None
    model: str = "gpt-5-nano"
    parallel_tool_calls: bool = True
    #previous_response_id: str = None
    prompt: object = None
    prompt_cache_key: str = None
    reasoning: str = '{"effort": "minimal"}'
    service_tier: str = "auto"
    store: bool = True
    stream: bool = True
    stream_options: object = None
    temperature: int = 1
    text: object = None
    tool_choice: str = None
    #tools: array = None
    top_logprobs: int = None
    top_p: int = 1
    truncation: str = None

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def to_class(cls, data: dict):
        data["reasoning"] = "{" + data["reasoning"].replace("'", "\"") + "}" #turns provided reasoning class string into a parseable json object
        return cls(**data)

    def update_settings(self, console, *args):
        #For now, args cannot be passed so this branch will always execute
        mod_settings = ""
        annotations = self.__class__.__annotations__
        dictionary = self.to_dict()
        if not args:
            #dictionary.pop("profile_name", None) #Remove the profile name from settings list.
            settings_list = "\n".join(f"{key}: {value} - of type [bold underline white]{annotations[key].__name__}[/bold underline white]" if key in annotations else "" for key, value in dictionary.items())
            console.print(f"[bold blue]Prompt Configurations\nEnter the settings you'd like the adjust, or type 'a' for all.[/bold blue]\n" + f"[bold blue]{settings_list}[/bold blue]")
            mod_settings = prompt(f">> ", style=meta.INPUT_STYLE).lower()
            if mod_settings == "a":
                mod_settings = dictionary.keys()
            else:
                mod_settings = mod_settings.replace(",", "").split(" ")
        if args:
            mod_settings =     args[0][::2]
            mod_setting_args = args[0][1::2]
            #print(mod_settings)
            #print(mod_setting_args)

        #FIXME: This needs to have the option for a user to provide the updating argument for the provided setting being changed.
        # e.g : !configure max_output_tokens 300
        for i, key in enumerate(mod_settings):
            if key in dictionary:
                if mod_setting_args[i] is not None:
                    updated_value = str(f"\"{mod_setting_args[i]}\"")
                else:
                    updated_value = prompt(f"Changing {key} (currently {dictionary[key]}, enter '#' to leave unchanged.): ")

                if updated_value.lower() == "none":
                    updated_value = None
                elif updated_value.lower() == "#":
                    updated_value = dictionary[key]
                else:
                    expected_type = annotations[key]
                    try:
                        if expected_type == bool:
                            updated_value = updated_value.lower() in ["true", "1", "yes"]
                        elif expected_type == int:
                            updated_value = int(updated_value)
                        elif expected_type == float:
                            updated_value = float(updated_value)
                    except ValueError as e:
                        console.print(f"{e}")
                dictionary[key] = updated_value
            else:
                console.print(f"[bold red]Invalid field {key}[/bold red]")
        self.__dict__.update(dictionary)

    def jsonify(self) -> str:
        return json.dumps(self.to_dict(), indent=4)