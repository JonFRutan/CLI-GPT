import re
import src.meta as meta
#is prompt.py even needed? Why not handle it all in creator.py?
class PromptGen:
    def __init__(self, file_manager):
        self.file_manager = file_manager
    
    #FIXME; Implement a switch for disabling the meta context.
    def generate (self, body):
        def replace(match):
            ref = match.group(1)
            #FIXME - CHANGE FROM meta INTO file_manager
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