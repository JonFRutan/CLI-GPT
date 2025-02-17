## CLI-GPT
CLI-GPT is a simple command-line frontend for using OpenAI's API.  
OpenAI's API is quite a bit more powerful than the standard ChatGPT frontend, allowing more customization to the model and fine control over generation aspects.  
I started CLI-GPT for use on a (console-only) FreeBSD install.

##### Goals  
I have three goals with CLI-GPT:    
 - *Simplicity* - CLI-GPT will be simple and intuitive.
 - *Customization* - CLI-GPT will be highly modifiable. 
 - *Universality* - CLI-GPT will run on anything.  

CLI-GPT has just started, and we have a long way to go before it reaches these goals.  
Ideally, CLI-GPT will download to any device (embedded, GUI-less, etc.) and be tailored to any need; such as automating tasks or just answering questions.   

##### Setup
Using this program requires an [OpenAI account](https://platform.openai.com/) (not to be confused with a ChatGPT account), and will require an API key which can be found [here](https://platform.openai.com/api-keys). This requires you add some funds to the account in order to qualify for making API calls.  
*Using gpt-4o-mini, my cumulative API calls have not even amounted to 1 cent. My use is generally restricted to testing the program though.*  
Once downloaded, you'll need [openai](https://pypi.org/project/openai/) and [rich](https://pypi.org/project/rich/). Then you can run ```python cli.py``` to use the program.  
Upon your first time running, it will ask for your API key, then it should prompt you to save it to your system.  

##### Using files
You can import file references into the program using the '!import' command.  
Every import will be given a reference name, chosen by you upon importing.  
To use an imported file, insert it into your prompt inside curly braces.  
Example:  
```
[> !import docs/text/notes.txt
docs/text/notes.txt found. Provide a reference name: notes
[> Correct spelling errors: {notes} 
```  
##### To Do
- Settings persistence (Currently WIP)
- File upload (Currently WIP)
- Auto-install scripts (Container/Venv)
- Image Generation
- Chats
- Automation

###### Contact
If you have any questions or issues please reach out to me through GitHub.  
I'm still learning, so don't hesitate to provide feedback if you have suggestions.  
