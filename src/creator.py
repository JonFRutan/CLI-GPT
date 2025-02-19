#NOTE;
# creator.py should offload it's settings into settings.py, and instead solely call the API for generation.
# creator should hold the PromptGen object.
import openai, re
import src.meta as meta
import itertools

class Creator:
    #FIXME; Replace these parameters with a single PromptSettings object
    def __init__(self, environment, key):
        self.payloader = Payload(environment.file_manager, environment.payload_config)
        if not key or not self.validate_key(key):
            return self.authenticate()
    
    def refresh(self, payload_config):
        self.payload_config = payload_config

    def generate_response(self, prompt):
        if not self.ai_client:
            return "API Client Error."
        payload = self.payloader.generate(prompt)
        try:
            response = self.ai_client.chat.completions.create(**payload)
            return response
        except openai.APIError as e:
            print(e)
            
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

#Payload will house a tuple of all necessary settings and file uploads
#It should serve directly into generate_response as such: creator.generate_response(payload)
#Does Payload need to redefine every option? Can it just include a modifiable copy of the provided payload_config?
class Payload:
    def __init__(self, file_manager, payload_config):
        self.file_manager = file_manager
        self.payload_config = payload_config.to_dict()
        
    def generate(self, prompt):
        #Check for image file imports
        #If image file imports included, modify sys_prompt to include a file_include argument
        body = self.generate_prompt(prompt)
        sys_prompt = self.payload_config.get("sys_prompt")
        configs = {k: v for k, v in self.payload_config.items() if k != "sys_prompt"}
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": body}
        ]

        if "response_format" in configs:
            configs["response_format"] = {"type": configs["response_format"]}

        payload = {**configs, "messages": messages}
        return payload
    
    def unroll(self, **kwargs):
        pass

    def preview(self):
        pass

    def generate_prompt (self, body):
        def replace(match):
            ref = match.group(1)
            if ref in self.file_manager.imported_files:
                file_contents = self.file_manager.retrieve_file(ref)
                #Meta context?
                return file_contents
            else:
                return None
        replacing_text = re.sub(meta.VAR_REGEX, replace, body)
        if replacing_text: 
            return replacing_text
        else:
            return 