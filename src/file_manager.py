import os 
import src.meta as meta
import base64

class ImportedFile:
    def __init__(self, ref, path, type):
        self.ref = ref
        self.path = path
        self.type = type
        if type in meta.IMAGE_FILES:
            self.base_value = None

class FileManager:
    def __init__(self):
        self.imported_files = {}
        #Any other info needed here?

    #returns file type for telling what was just brought in.
    def import_file(self, file_path, name):
        #May be removed, but keeping it to double-check for now
        if not os.path.isfile(file_path):
            print (f"File {file_path} doesn't exist.")
            return None
        #NOTE; you can also use os.path.splitext to get the filetype.
        file_type = file_path[::-1].split(".")[0][::-1]   #Reverses, cuts at period, slices, reverses again
        if file_type not in meta.IMAGE_FILES and file_type not in meta.TEXT_FILES:
            return f"{file_path} has invalid type: {file_type}"
        self.imported_files[name] = ImportedFile(name, file_path, file_type)
        return f"{file_path} -> {name}"
    
    def retrieve_file(self, ref):
        if ref in self.imported_files:
            working_file = self.imported_files[ref]
            if working_file.type in meta.TEXT_FILES:
                with open (working_file.path, 'r') as file:
                    return file.read()
            elif working_file.type in meta.IMAGE_FILES:  
                with open (working_file.path, "rb") as image:
                    return base64.b64encode(image.read()).decode("utf-8")
            #NOTE; Image uploads are handled differently by the API, so this won't work
            #OpenAI's API handles image uploads as seperate parts of the payload.
        else:
            print(f"Reference {ref} unknown.")

    def export_file(self, file_content, file_name, dest):
        destination = dest + file_name
        print(f"{destination} and {file_content}")
        try:
            with open(destination, "w") as file:
                file.write(file_content)
            return f"File created at {destination}"
        except Exception as e:
            return f"File export error. - {e}"