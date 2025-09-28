import openai, re, json
import src.meta as meta

class Creator:
    def __init__(self, environment, key):
        self.environment = environment
        self.payloader = Payload(environment.file_manager, environment.prompt_config)
        if not key or not self.validate_key(key):
            return self.authenticate()
    
    def refresh(self):
        self.payloader.payload_config = self.environment.prompt_config.to_dict()

    def generate_response(self, prompt):
        if not self.ai_client:
            return "API Client Error."
        payload = self.payloader.generate(prompt)
        if not payload:
            print("Error in in generate_response.")
            return None
        try:
            response = self.ai_client.responses.create(**payload)
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
        vars = re.findall(meta.VAR_REGEX, prompt)
        image_code = None
        for var in vars:
            reference = self.file_manager.imported_files.get(var.strip("{}"))
            if reference.type in meta.IMAGE_FILES:
                image_code = f"data:image/{reference.type};base64,{self.file_manager.retrieve_file(var)}"
        body = self.generate_prompt(prompt)
        if not body:
            print("Generated body is 'None' - Payload.generate")
            return None
        instructions = self.payload_config.get("instructions")
        configs = {k: v for k, v in self.payload_config.items() if k not in ["instructions", "reasoning"]}
        #When importing images, we must change the content from 'body' to a dictionary containing:
        # "type" : "text", "text": body
        # "type" : "image_url", "image_url": {"url": image_url}
        # The idea for now is to create a user_message dictionary object, this will be in generate_user_message

        if "response_format" in configs:
            configs["response_format"] = {"type": configs["response_format"]}
        reasoning_object = json.loads(self.payload_config["reasoning"])
        payload = {**configs, "instructions": instructions, "input": body, "reasoning": reasoning_object}
        if payload is None:
            print("Unloaded configs resulted in empty payload - Payload.generate")
        return payload

    def generate_user_message (self):
        pass

    def generate_prompt (self, body):
        def replace(match):
            ref = match.group(1)
            if ref in self.file_manager.imported_files:
                file_contents = self.file_manager.retrieve_file(ref)
                #Meta context?
                return file_contents
            else:
                return ""
        replacing_text = re.sub(meta.VAR_REGEX, replace, body)
        if replacing_text: 
            return replacing_text
        else:
            return None