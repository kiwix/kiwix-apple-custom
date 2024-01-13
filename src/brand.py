from pathlib import Path
import sys

INFO_JSON = 'info.json'

class Brand:
    
    def __init__(self, name):
        if Path(name).is_dir() == False:
            self._exit_with_error(f"The directory of the brand: '{name}' does not exist")
        self.info_file = Path(name)/INFO_JSON
        if self.info_file.exists() == False:
            self._exit_with_error(f"There is no {INFO_JSON} file for brand {name}")
        self.name = name
        
    @staticmethod
    def all_info_files():
        return list(Path().rglob(INFO_JSON))
        
    def _exit_with_error(self, msg):
        print(f"Error: {msg}")
        sys.exit(1)
