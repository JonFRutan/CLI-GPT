import src.file_manager as filem
import src.meta as meta

from prompt_toolkit import prompt
from dataclasses import dataclass
from typing import Optional, Union

import json
# The goal of environment.py is to encapsulate both API settings (tokens, system prompt, temp, etc) and the user's client settings (disabling welcome message, enabling persistent file imports, etc.) into one settings object.
# JSON will be used for settings storage, as it's easily maintainable and a user may edit it manually if need be.

class Environment:
    def __init__(self, console):
        self.console = console
        #Upon init, Environment should check for a JSON file containing already existing modifications.
        self.payload_config = None
        self.user_settings = None
        self.file_manager = filem.FileManager()
        #TRY IMPORTING A SETTINGS JSON HERE FOR PROMPT_CONFIG
        #Saved profiles should be saved in a format where they can directly be rolled into an argument put below
        self.prompt_config = PromptProfile()

    def print_settings(self):
        return (f"Model: {self.payload_config.model}\nSystem Prompt: {self.payload_config.sys_prompt}")
    
    def update_settings(self):
        meta.clear_screen()
        self.console.print("[bold red]Settings[/bold red]\n[bold red]Select a menu:[/bold red]\nProgram settings (u)\nPrompt settings (p)")
        response = prompt(">> ").lower()
        if response == "u":
            return self.user_settings.update_settings(self.console)
        elif response == "p":
            return self.payload_config.update_settings(self.console)

#No user settings are currently implemented
class UserSettings:
    def __init__(self):
        pass
    def update_settings(self, console):
        pass

@dataclass
class PromptProfile:
    model: str = "gpt-4o-mini"
    sys_prompt: str = "Be brief. Keep it to plain text."
    stream: bool = True
    max_tokens: int = 200
    temperature: float = 0.6
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: Optional[Union[str, list]] = None
    logprobs: Optional[bool] = None
    echo: bool = False
    response_format: str = "text"
    seed: Optional[int] = None

    #NOTE; update_settings should accept an argument(?) for settings to iterate through and change.
    def update_settings(self, console):
        console.print("Updating prompt settings- type '#' to leave a setting unchanged.")
        #model
        while True:
            new_model = console.input("What model would you like to use? (Type '?' to list options) -> ")
            if new_model == '#':
                break
            elif new_model == '?':
                console.print(f"Ordered by token pricing: {meta.API_MODELS_LIST}")
            elif new_model in meta.API_MODELS_LIST:
                self.model = new_model
                break
        #sys_prompt
        while True:
            new_system = console.input("Provide a new system prompt ('?' for help) -> ")
            if new_system == '#':
                break
            elif new_system == '?':
                console.print("The system settings affects the models behavior.\nThe default is 'Be a bit brief. When formatting text avoid markdown and use plain text.'\nYou can modify this to your liking, e.g. 'Your responses will strictly be in JSON format.'")
            else:
                self.sys_prompt = new_system
                break