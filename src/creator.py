#NOTE;
# creator.py should offload it's settings into settings.py, and instead focus simply on calling the API for generation.

import openai
import meta as meta

class Creator:
    def __init__(self, model, system_settings, ai_client):
        self.model = model
        self.system_settings = system_settings
        self.ai_client = ai_client
    
    def print_settings(self):
        return (f"Model: {self.model} | System: {self.system_settings}")
    
    def update_settings(self):
        self.print_settings()
        print("Updating settings- type '#' to leave a setting unchanged.")

        #Model
        while True:
            new_model = input("What model would you like to use? (Type '?' to list options) -> ")
            if new_model == '#':
                break
            elif new_model == '?':
                print(f"Ordered by token pricing: {meta.MODEL_LIST}")
            elif new_model in meta.MODEL_LIST:
                self.model = new_model
                break

        #System
        while True:
            new_system = input("Provide a new system prompt ('?' for help) -> ")
            if new_system == '#':
                break
            elif new_system == '?':
                print("The system settings affects the models behavior.\nThe default is 'Be a bit brief. When formatting text avoid markdown and use plain text.'\nYou can modify this to your liking, e.g. 'Your responses will strictly be in JSON format.'")
            else:
                self.system_settings = new_system
                break

    def generate_response(self, prompt):
        response = self.ai_client.chat.completions.create(
            model=f"{self.model}",
            store=True,
            messages=[
            {"role": "system", "content": f"{self.system_settings}"},
            {"role": "user", "content": f"{prompt}"}],
            stream=True,
            #max_tokens = 200, #Response length (higher -> longer)
            #temperature = .5, #Randomness (0.0 is deterministic, 1.0 is very random)
            #top_p = 1.0, #Nucleus sampling (0.0 only considers most likely tokens)
            #frequency_penalty = 0.0, #Penalty value to frequent words (-2.0 to 2.0, higher is more penalty to repetition)
            #presence_penalty = 0.0, #Encourages new topic introduction (-2.0 to 2.0, higher makes it more diverse)
            #stop=["###", "\n\n"], #Stopping sequence, cuts responses early if encountered.
            #logprobs = None, #
            #echo - False, #True will include the prompt in the response, false doesn't.
            #response_format = "json", #Makes response strictly adhere to a given format
            #seed=40, #Deterministic responses for the same inputs
        )
        return response

    def validate_key(self, api_key):
        try:
            test_client = openai.OpenAI(api_key=api_key)
            test_client.models.list()
            self.ai_client = test_client
        except openai.BadRequestError:
            print("Invalid API key.")
            self.ai_client = None
        except Exception as e:
            print(f"API Issue. Try reentering your API key.\nError: {e}")
            self.ai_client = None