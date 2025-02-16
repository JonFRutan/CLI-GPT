from enum import Enum, auto

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