import re, meta
class Prompt:
    def __init__(self, body):
        self.body = body
        self.body = self.prompt_process(body) 
    
    def prompt_process (self, body):
        def replace(match):
            ref = match.group(1)
            if ref in meta.IMPORTED_FILES:
                file_contents = meta.retrieve_file(ref)
                return f"\n#META: A FILE REFERRED TO AS {ref} STARTS HERE#\n" + file_contents + f"\n#META: THE FILE REFFERED TO AS {ref} ENDS HERE#\n"
            else:
                return None
        replacing_text = re.sub(meta.VAR_REGEX, replace, body)
        if replacing_text: 
            return replacing_text
        else:
            return 