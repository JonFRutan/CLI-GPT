## CLI-GPT
CLI-GPT is a simple command-line frontend for using OpenAI's API.  
OpenAI's API is quite a bit more powerful than the standard ChatGPT frontend, allowing more customization to the model and fine control over generation aspects.  
The goal of CLI-GPT is to provide a simple and intuitive interface for using and customizing OpenAI's API all from your terminal, useful for devices without a windowing system installed.
##### Setup:
Using this program requires an [OpenAI account](https://platform.openai.com/) (not to be confused with a ChatGPT account), and will require an API key which can be found [here](https://platform.openai.com/api-keys). This requires you add some funds to the account in order to qualify for making API calls.  
*Using gpt-4o-mini, my cumulative API calls have not even amounted to 1 cent. My use is generally restricted to testing the program though.*  
Once downloaded, you'll need [openai](https://pypi.org/project/openai/) and [rich](https://pypi.org/project/rich/). Then you can run ```python cli.py``` to use the program.  
Upon your first time running, it will ask for your API key, then it should prompt you to save it to your system.  
If you run into any problems, please reach out to me or create an issue.  
##### Using files:
You can import file references into the program using the '!import' command.  
Every import will be given a reference name, chosen by you upon importing.  
To use an imported file, insert it into your prompt inside curly braces.  
E.g.  
```[> !import docs/text/notes.txt
src/tests/file1.txt found. Provide a reference name: notes
[> Correct spelling errors: {notes}```  
##### To Do:
- Settings persistence
- Auto-install scripts (Container/Venv)
- Image Generation
- Image/File upload (WIP)
- Chats
