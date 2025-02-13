import openai
import globals

class UserClient:
    def __init__(self, model, system_settings, ai_client):
        self.model = model
        self.system_settings = system_settings
        self.ai_client = ai_client
    
    def print_settings(self):
        print(f"Model: {self.model} | System: {self.system_settings}")
    
    def update_settings(self):
        self.print_settings()
        print("Updating settings- type '#' to leave a setting unchanged.")

        #Model
        while True:
            new_model = input("What model would you like to use? (Type '?' to list options) -> ")
            if new_model == '#':
                break
            elif new_model == '?':
                print(f"Ordered by token pricing: {globals.MODEL_LIST}")
            elif new_model in globals.MODEL_LIST:
                self.model = new_model
                break

        #System
        while True:
            new_system = input("Provide a new system prompt ('?' for help) -> ")
            if new_system == '#':
                break
            elif new_system == '?':
                print("The system settings affects the models behavior.\nThe default is 'Be a bit brief. When formatting text avoid markdown and use plain text.'\nYou can modify this to your liking, e.g. 'Your responses will strictly be in alphabetic ciphers'")
            else:
                self.system_settings = new_system
                break
