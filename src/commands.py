import os
import src.meta as meta

from prompt_toolkit import prompt

#Command name, description, usage, and related function
class Command:
    def __init__ (self, name, description, syntax, action, context=None):
        self.name = name
        self.description = description
        self.syntax = syntax
        self.action = action
        self.context = context

    def execute(self, *args, **kwargs):
        if args:
            self.context = args
            return self.action(self.context, *args, **kwargs)
        elif self.action:
            return self.action(*args, **kwargs)
        else:
            raise ValueError(f"No action defined for {self.name}")

#Command functions
#FIXME; user_creator will be defunct. All references to it in terms of user settings should be refactored into environment.py other classes
class Commands:
    def __init__(self, environment, creator):
        self.environment = environment
        self.creator = creator
        self.commands = self.populate_commands()
    
    def clear_screen(self, *args):
        meta.clear_screen()
        return "[bold cyan]CLI-GPT[/bold cyan]\nType '!exit' or hit Ctrl+C to exit the program.\nType '!help' to see more commands."

    #FIXME - This command is too general, it should be made more robust.
    # Instead of calling the creator object, info should accept arguments as to specific details or subcategoires like "PromptSettings" or "UserSettings"
    def show_info(self, *args):
        config = self.creator.payloader.payload_config
        return "\n".join(f"{key}: {value}" for key, value in config.items())

    def show_help(self, *args):
        if not args:
            return "Available commands:\nType !help (any command) to learn more about a specific commmand. \n" + "\n".join(f"'{cmd.name}' - {cmd.description}" for cmd in self.commands.values())
        c = "!" + args[0][0] 
        if c in self.commands:
            return f"{self.commands[c].name} - {self.commands[c].description} \nUsage: {self.commands[c].syntax}"
        else:
            return "Unknown command"

    def import_file(self, *args):
        appender = ""
        if not args:
            return f"No arguments provided. Usage: {self.commands["!import"].syntax}"
        for path in args[0]:
            if os.path.isfile(path):
                file_name = prompt(f"{path} found; provide a reference name: ", style=meta.INPUT_STYLE)
                appender += self.environment.file_manager.import_file(path, file_name)
        return appender
    
    def configure(self, *args):
        #Needs to handle args
        self.environment.update_settings()
        #Refreshing every time for now
        return self.clear_screen()

    def export_profile(self, *args):
        if args:
            return self.environment.export_profile(args[0][0])
        
    def show_imports(self, *args):
        appender = ""
        for entry in self.environment.file_manager.imported_files:
            file_ref = self.environment.file_manager.imported_files[entry]
            appender += f"{file_ref.ref} ({file_ref.path}), "
        if appender == "":
            return "No references yet. Use !import"
        return appender
    
    #List of command items
    #To add, remove, or change commands; modify this function.
    def populate_commands(self):
        commands = {
            "!help": Command("help", "List available commands.", "!help  OR !help (command)" , self.show_help),
            "!info": Command("info", "Display user/system information.", "!info", self.show_info),
            "!clear": Command("clear", "Clear the screen.", "clear", self.clear_screen),
            "!import": Command("import", "Import a file. Import is used in conjunction with references", "import files/image.png", self.import_file),
            "!configure": Command("configure", "Manually adjust all system settings", "!configure OR !configure (setting)", self.configure),
            "!references": Command("references", "Show local file references. Imported files can be used in prompting.", "!references || > 'Correct spelling errors from: {reference}.'", self.show_imports),
            "!export": Command("export", "Export the current profile as a JSON. Arguments will name the profile.", "!export very_random", self.export_profile),
            #"": Command(),
        }
        return commands