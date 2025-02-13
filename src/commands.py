import meta

class Command:
    def __init__ (self, name, description, syntax, action, context=None):
        self.name = name
        self.description = description
        self.syntax = syntax
        self.action = action
        self.context = context

    def execute(self, *args, **kwargs):
        #Optional arguments are allowed
        if self.action:
            if self.context:
                return self.action(self.context, *args, **kwargs)
            return self.action(*args, **kwargs)
        else:
            raise ValueError(f"No action defined for {self.name}")


#NOTE: When incorporating a library for a CLI interface commands like clear_screen may be defunct.
#Command functions
class Commands:
    def __init__(self, user):
        self.user = user
        self.populate_commands(user)
    
    #FIXME; Doesn't work
    def clear_screen(self):
        meta.clear_screen

    def show_info(self):
        return self.user.print_settings()

    def show_help(self):
        return "Available commands: \n" + "\n".join(f"'{cmd.name}' - {cmd.description}" for cmd in self.commands.values()) 

    def import_file(self):
        pass
    
    def update_settings(self):
        self.user.update_settings()

    #List of command items
    #To add, remove, or change commands; modify this function.
    def populate_commands(self, user):
        self.commands = {
            "!help": Command("!help", "List available commands.", "help" , self.show_help),
            "!info": Command("!info", "Display user/system information.", "info", self.show_info),
            "!clear": Command("!clear", "Clear the screen.", "clear", self.clear_screen),
            "!import": Command("!import", "Import a file", "import files/image.png", self.import_file),
            "!configure": Command("!configure", "Manually adjust all system settings", "!configure", self.update_settings),
            #"": Command(),
        }
        return self.commands