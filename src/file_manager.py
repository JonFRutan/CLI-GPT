#FIXME; File import/retrieval should be handled here. Refactor away from meta.py...
import os 
import src.meta as meta
class ImportedFile:
    def __init__(self, ref, path, type):
        self.ref = ref
        self.path = path
        self.type = type

class FileManager:
    def __init__(self):
        self.imported_files = {}
        #Any other info needed here?

    def import_file(self, file_path):
        if not os.path.isfile(file_path):
            print (f"File {file_path} doesn't exist.")
            return None
        file_type = file_path[::-1].split(".")[0][::-1]   #Reverses, cuts at period, slices, reverses again
        #NOTE; you can also use os.path.splitext to get the filetype, but I already made this.
        reference_name = input(f"{file_path} found. Provide a reference name: ").strip()
        self.imported_files[reference_name] = ImportedFile(reference_name, file_path, file_type)
        return 1
    
    def retrieve_file(self, ref):
        if ref in self.imported_files:
            working_file = self.imported_files[ref]
            if working_file.type in meta.TEXT_FILES:
                with open (working_file.path, 'r') as file:
                    return file.read()
            elif working_file.type in meta.IMAGE_FILES:  
                pass     
        else:
            print(f"Reference {ref} unknown.")