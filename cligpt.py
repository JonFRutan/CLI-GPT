#jfr
import sys, os, platform
import openai 
import user_client, globals

def validate_key(api_key):
    try:
        client = openai.OpenAI(api_key=api_key)
        client.models.list()
        return client
    except openai.BadRequestError:
        print("Invalid API key.")
        return False
    except Exception as e:
        print("API Issue. Try reentering your API key.")
        return False

def generate_response(user, prompt):
    response = user.ai_client.chat.completions.create(
        model=f"{user.model}",
        store=True,
        messages=[
        {"role": "system", "content": f"{user.system_settings}"},
        {"role": "user", "content": f"{prompt}"}],
        stream=True
    )
    return response

globals.clear_screen()
print("Connecting to API...")
user = user_client.UserClient("gpt-4o-mini", "Be a bit brief. When formatting text avoid markdown and use plain text.", None)
ready = True
key = os.getenv("OPENAI_API_KEY")
if key:
    user.ai_client = validate_key(key)   
if not key:
    ready = False
globals.clear_screen()

while not ready:
    api_key = input("Please provide your OpenAI API key (? for help, x for exit.): ")
    if api_key == "?":
        print("Navigate to platform.openai.com, sign in, under PROJECT is an API key section.")
    elif api_key == 'x':
        exit()
    else:
        user.ai_client = validate_key(api_key)
        if user.ai_client:
            ready = True
            save = input("Would you like to save the key to your system environment? (y/n)")
            if save == 'y':
                globals.save_environment_variable(api_key)
globals.clear_screen()

commands = {
    "configure": user.update_settings,
    "info": user.print_settings,
}

print("CLI-GPT\nType 'exit' or hit Ctrl+C to exit the program.\nType 'help' to see more commands.", end="")
while True:    
    prompt = input("\n> ")
    if prompt == "exit":
        exit()
    elif prompt == "help":
        print(f"Available Commands:\n'configure' - Update model and system prompt.\n'info' - Prints some relevant info like model and prompt.")
    elif prompt in commands:
        commands[prompt]()
    else:
        response = generate_response(user, prompt)
        for chunk in response:
            buffer = chunk.choices[0].delta.content
            if buffer:
                print(buffer, end="")
