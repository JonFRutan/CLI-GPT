import re, meta
class Prompt:
    def __init__(self, body):
        self.body = body
        self.body = self.prompt_process(body) 
    
    #FIXME; Implement a switch for disabling the meta context.
    def prompt_process (self, body):
        def replace(match):
            ref = match.group(1)
            if ref in meta.IMPORTED_FILES:
                file_contents = meta.retrieve_file(ref)
                #Meta context- There should be an option for a user to disable this.
                return f"\n#META: A FILE REFERRED TO AS {ref} STARTS HERE#\n" + file_contents + f"\n#META: THE FILE REFFERED TO AS {ref} ENDS HERE#\n"
            else:
                return None
        replacing_text = re.sub(meta.VAR_REGEX, replace, body)
        if replacing_text: 
            return replacing_text
        else:
            return 