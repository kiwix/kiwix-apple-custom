from pathlib import Path

INFO_JSON = 'info.json'


class Brand:

    def __init__(self, name):
        if Path(name).is_dir() == False:
            raise FileExistsError(
                f"The directory for brand: '{name}' does not exist")
        self.info_file = Path(name)/INFO_JSON
        if self.info_file.exists() == False:
            raise FileExistsError(
                f"There is no {INFO_JSON} file for brand '{name}'")

        self.name = name

    @staticmethod
    def all_info_files():
        return list(Path().rglob(INFO_JSON))
