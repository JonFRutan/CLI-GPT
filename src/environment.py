from enum import Enum
from creator import Creator
import file_manager as filem
import meta
import json
#NOTE;
# The goal of environment.py is to encapsulate both API settings (tokens, system prompt, temp, etc) and the user's client settings (disabling welcome message, enabling persistent file imports, etc.) into one settings object.
# I will have subdivided responsibilites among the settings classes, all beholden to the greater Settings object.
# JSON will be used for settings storage, as it's easily maintainable and a user may edit it manually if need be.

class Environment:
    def __init__(self):
        #Upon init, Environment should check for a JSON file containing already existing modifications.
        self.prompt_config = None
        self.user_settings = None
        self.file_manager = filem.FileManager()
        self.default_profile =("gpt-4o-mini", "Be a bit brief. When formatting text avoid markdown and use plain text.", None)
        #FIXME
        #TRY IMPORTING A SETTINGS JSON HERE FOR PROMPT_CONFIG#
        #FIXME
        if not self.prompt_config:
            self.prompt_config = PromptConfig(*self.default_profile)
        self.creator = Creator(self.prompt_config)

    def print_settings(self):
        return (f"Model: {self.prompt_config.model}\nSystem Prompt: {self.prompt_config.sys_prompt}")
    
    def authenticate(self):
        while True:
            api_key = input("Please provide your OpenAI API key (? for help, x to exit.): ")
            if api_key == "?":
                print("Navigate to platform.openai.com, sign in, under PROJECT is an API key section.")
            elif api_key.lower() == 'x':
                print("Exiting...")
                exit()
            else:
                self.creator.validate_key(api_key)
                if self.creator.ai_client:
                    save = input("Would you like to save the key as a system environment variable? (y/n)")
                    if save.lower() == 'y':
                        meta.save_environment_variable(api_key)
                return


class UserSettings(Enum):
    pass

class PromptConfig:
    def __init__(self, model, sys_prompt, api_client):
        self.model = model
        self.sys_prompt = sys_prompt
        self.api_client = api_client
        