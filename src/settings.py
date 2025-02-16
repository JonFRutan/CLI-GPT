from enum import Enum, auto
#NOTE;
# The goal of settings is to encapsulate both API settings (tokens, system prompt, temp, etc) and the user's client settings (disabling welcome message, enabling persistent file imports, etc.) into one settings object.
# I will have subdivided responsibilites among the settings classes, all beholden to the greater Settings object.
# JSON will be used for settings storage, as it's easily maintainable and a user may edit it manually if need be.

class Settings:
    def __init__(self):
        self.prompt_settings = {

        }
        
class UserSettings(Enum):
    pass

class PromptSettings(Enum):
    MAX_TOKENS = auto()
    TEMPERATURE = auto()
    TOP_P = auto()
    FREQUENCY_PENALTY = auto()
    PRESENCE_PENALTY = auto()
    STOP_SEQUENCES = auto()
    RESPONSE_FORMAT = auto()
    SEED = auto()