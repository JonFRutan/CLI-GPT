import meta

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
        elif args[0][0] in self.commands:
            c = args[0][0]
            return f"{self.commands[c].name} - {self.commands[c].description} - Usage: {self.commands[c].syntax}"
        else:
            return "Unknown command"

    def import_file(self, *args):
        if not args:
            return f"No arguments. Usage: {self.commands["!info"].syntax}"
        else:
            appender = ""
            for path in args[0]:
                appender += meta.import_file(path)
        return appender
    
    def update_settings(self):
        self.user.update_settings()

    #List of command items
    #To add, remove, or change commands; modify this function.
    def populate_commands(self, user):
        self.commands = {
            "!help": Command("!help", "List available commands.", "!help  OR !help !(command)" , self.show_help),
            "!info": Command("!info", "Display user/system information.", "!info (filepath1) ... (filepathX)", self.show_info),
            "!clear": Command("!clear", "Clear the screen.", "clear", self.clear_screen),
            "!import": Command("!import", "Import a file", "import files/image.png", self.import_file),
            "!configure": Command("!configure", "Manually adjust all system settings", "!configure OR !configure (setting)", self.update_settings),
            #"": Command(),
        }
        return self.commands