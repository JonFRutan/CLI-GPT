#NOTE;
# creator.py should offload it's settings into settings.py, and instead solely call the API for generation.
# creator should hold the PromptGen object.
import openai
from src.prompt import PromptGen
import src.meta as meta

class Creator:
    #FIXME; Replace these parameters with a single PromptSettings object
    def __init__(self, prompt_config, file_manager):
        self.model = prompt_config.model
        self.sys_prompt = prompt_config.sys_prompt
        #Should api_client be a part of prompt_config? This should be changed into solely a Creator attribute.
        self.ai_client = None
        self.prompter = PromptGen(file_manager)
    
    def refresh(self, prompt_config):
        self.model = prompt_config.model
        self.sys_prompt = prompt_config.sys_prompt

    def generate_response(self, prompt):
        if not self.ai_client:
            return "API Client Error."
        full_prompt = self.prompter.generate(prompt)
        response = self.ai_client.chat.completions.create(
            model=f"{self.model}",
            store=True,
            messages=[
            {"role": "system", "content": f"{self.sys_prompt}"},
            {"role": "user", "content": f"{full_prompt}"}],
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
            return True
        except openai.BadRequestError:
            print("Invalid API key.")
            return False
        except Exception as e:
            print(f"API Issue. Try reentering your API key.\nError: {e}")
            return False
        
    def authenticate(self):
        while True:
            api_key = input("Please provide your OpenAI API key (? for help, x to exit.): ")
            if api_key == "?":
                print("Navigate to platform.openai.com, sign in, under PROJECT is an API key section.")
            elif api_key.lower() == 'x':
                print("Exiting...")
                exit()
            else:
                if self.validate_key(api_key):
                    save = input("Would you like to save the key as a system environment variable? (y/n)")
                    if save.lower() == 'y':
                        return meta.save_environment_variable(api_key)
                    else: 
                        return "API Key Accepted."
                else:
                    print("Something went wrong...")