import src.file_manager as filem
import src.meta as meta

from prompt_toolkit import prompt
from dataclasses import dataclass
from typing import Optional, Union

import json
# The goal of environment.py is to encapsulate both API settings (tokens, system prompt, temp, etc) and the user's client settings (disabling welcome message, enabling persistent file imports, etc.) into one settings object.
# JSON will be used for settings storage, as it's easily maintainable and a user may edit it manually if need be.

class Environment:
    def __init__(self, console, *args):
        self.console = console
        #Upon init, Environment should check for a JSON file containing already existing modifications.
        self.user_settings = None
        self.prompt_config = PromptProfile()
        self.file_manager = filem.FileManager()
        #TRY IMPORTING A SETTINGS JSON HERE FOR PROMPT_CONFIG
        #Saved profiles should be saved in a format where they can directly be rolled into an argument put below

    def print_settings(self):
        return (f"Model: {self.prompt_config.model}\nSystem Prompt: {self.prompt_config.sys_prompt}")
    
    def export_profile(self, name):
        return self.file_manager.export_file(self.prompt_config.jsonify(), name+".json", "src/profiles/")

    def update_settings(self):
        meta.clear_screen()
        self.console.print("[bold red]Settings[/bold red]\n[bold red]Select a menu:\nProgram settings (u)\nPrompt settings (p)[/bold red]")
        response = prompt(f">> ", style=meta.input_style).lower()
        if response == "u":
            return self.user_settings.update_settings(self.console)
        elif response == "p":
            return self.prompt_config.update_settings(self.console)

#No user settings are currently implemented
class UserSettings:
    def __init__(self):
        pass
    def update_settings(self, console):
        return "WIP"

#NOTE; It may be better to define a PromptParameter object and store the name, value, value type, and ranges.
@dataclass
class PromptProfile:
    model: str = "gpt-4o-mini"
    sys_prompt: str = "Be brief. Keep it to plain text."
    stream: bool = True
    store: bool = True
    max_tokens: int = 200
    temperature: float = 0.6
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: str = None
    logprobs: bool = None
    #echo: bool = False
    response_format: str = "text"
    seed: int = None

    def to_dict(self) -> dict:
        return self.__dict__
    
    @classmethod
    def to_class(cls, data: dict):
        return cls(**data)

    def update_settings(self, console, *args):
        #For now, args cannot be passed so this branch will always execute
        if not args:
            annotations = self.__class__.__annotations__
            dictionary = self.to_dict()
            #dictionary.pop("profile_name", None) #Remove the profile name from settings list.
            settings_list = "\n".join(f"{key}: {value} - of type [bold underline white]{annotations[key].__name__}[/bold underline white]" if key in annotations else "" for key, value in dictionary.items())
            console.print(f"[bold blue]Prompt Configurations\nEnter the settings you'd like the adjust, or type 'a' for all.[/bold blue]\n" + f"[bold blue]{settings_list}[/bold blue]")
            responses = prompt(f">> ", style=meta.input_style).lower()
            if responses == "a":
                responses = dictionary.keys()
            else:
                responses = responses.split(" ")
        if args:
            responses = args
        for key in responses:
            if key in dictionary:
                updated_value = prompt(f"Changing {key} (currently {dictionary[key]}): ")
                if updated_value.lower() == "none":
                    updated_value = None
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