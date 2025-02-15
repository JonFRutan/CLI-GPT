import re, meta
class Prompt:
    def __init__(self, body):
        self.body = body
        self.body = self.prompt_process(body) 
    
    def prompt_process (self, body):
        def replace(match):
            ref = match.group(1)
            if ref in meta.imported_files:
                return meta.retrieve_file(ref)
            else:
                return f"Error: {ref} not found."
        return re.sub(meta.var_reg, replace, body)