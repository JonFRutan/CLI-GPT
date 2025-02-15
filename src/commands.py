import meta, prompt

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


#NOTE: When incorporating a library for a CLI interface commands like clear_screen may be defunct.
#Command functions
class Commands:
    def __init__(self, user):
        self.user = user
        self.populate_commands(user)
    
    def clear_screen(self, *args):
        meta.clear_screen()
        return "[bold cyan]CLI-GPT[/bold cyan]\nType '!exit' or hit Ctrl+C to exit the program.\nType '!help' to see more commands."

    def show_info(self, *args):
        return self.user.print_settings()

    def show_help(self, *args):
        if not args:
            return "Available commands:\nType !help !(any command) to learn more about a specific commmand. \n" + "\n".join(f"'{cmd.name}' - {cmd.description}" for cmd in self.commands.values())
        c = "!" + args[0][0] 
        if c in self.commands:
            return f"{self.commands[c].name} - {self.commands[c].description} \nUsage: {self.commands[c].syntax}"
        else:
            return "Unknown command"

    def import_file(self, *args):
        if not args:
            return f"No arguments provided. Usage: {self.commands["!info"].syntax}"
        else:
            for path in args[0]:
                meta.import_file(path)
    
    def update_settings(self):
        self.user.update_settings()

    def show_imports(self, *args):
        appender = ""
        for entry in meta.imported_files:
            appender += entry + ", "
        return appender
    
    #List of command items
    #To add, remove, or change commands; modify this function.
    def populate_commands(self, user):
        self.commands = {
            "!help": Command("help", "List available commands.", "!help  OR !help !(command)" , self.show_help),
            "!info": Command("info", "Display user/system information.", "!info", self.show_info),
            "!clear": Command("clear", "Clear the screen.", "clear", self.clear_screen),
            "!import": Command("import", "Import a file. Import is used in conjunction with references", "import files/image.png", self.import_file),
            "!configure": Command("configure", "Manually adjust all system settings", "!configure OR !configure (setting)", self.update_settings),
            "!references": Command("references", "Show local file references. Imported files can be used in prompting.", "!references || > 'Correct spelling errors from: {reference}.'", self.show_imports),
            #"": Command(),
        }
        return self.commands