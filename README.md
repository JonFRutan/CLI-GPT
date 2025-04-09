## CLI-GPT

CLI-GPT is a simple command-line frontend for using OpenAI's API.  
OpenAI's API is quite a bit more powerful than the standard ChatGPT frontend, allowing more customization to the model and fine control over generation aspects. I started CLI-GPT for use on a headless FreeBSD system. It is written entirely in Python, although in the future I would like to look into refactoring into another (smaller footprint) language.  

#### Goals  

I have three goals with CLI-GPT:    
 - **Simplicity**    - CLI-GPT will be simple and intuitive.  
 - **Customization** - CLI-GPT will be highly modifiable.  
 - **Compatibility** - CLI-GPT will run on anything.  

CLI-GPT has just started, and we have a long way to go before it reaches these goals.  
Ideally, CLI-GPT will download to any device (embedded, GUI-less, etc.) and be tailored to any need; such as automating tasks or just answering questions.   

#### Setup

Using this program requires an [OpenAI account](https://platform.openai.com/) (not to be confused with a ChatGPT account), and will require an API key which can be found [here](https://platform.openai.com/api-keys). **This will require you to add credits to your account.** Don't fret though, I added $5 and my cumulative charges have amounted to a single cent (using gpt-4o-mini).  

##### Requirements

Once downloaded, you'll need [openai](https://pypi.org/project/openai/), [rich](https://pypi.org/project/rich/), and [prompt-toolkit](https://pypi.org/project/prompt-toolkit/). Then just run `python cli.py`.  
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
#### To Do

- Settings persistence (Prompt settings done.)
- File upload (Currently WIP)
- Auto-install scripts (Container/Venv)
- Image Generation
- Chats
- Automation

##### Contact

If you have any questions or issues please reach out to me through GitHub.  
I'm still learning, so don't hesitate to provide feedback if you have suggestions.  
