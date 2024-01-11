from glob import glob
from info_parser import InfoParser
import subprocess
import yaml


class CustomApps:

    def __init__(self):
        self.info_files = []
        for f in glob('./**/info.json', recursive=True):
            self.info_files.append(f)

    def create_custom_project_file(self, path="custom_project.yml"):
        """Create the project file based on the main repo project.yml
        It will contain the targets we need for each custom app, and their build settings,
        pointing to their individual info.plist files

        Args:
            path (str, optional): the output file path where it will be saved. Defaults to "custom_project.yml".
        """
        dict = {"include": ["project.yml"]}
        targets = {}
        for info in self.info_files:
            parser = InfoParser(info)
            targets = targets | parser.as_project_yml()

        dict["targets"] = targets
        with open(path, "w") as file:
            yaml.dump(dict, file)

    def create_plists(self, custom_plist):
        """Generate the plist files for each brand

        Args:
            custom_plist (string): the path to the original plist file we are basing this of,
            it should be a copy from the Kiwix target
        """
        for info in self.info_files:
            parser = InfoParser(info)
            parser.create_plist(based_on_plist_file=custom_plist)

    def download_zim_files(self):
        """Download all the zim files that were declared in the info.json files
        """
        for cmd in self._curl_download_commands():
            subprocess.call(cmd)

    # private
    def _curl_download_commands(self):
        """Yield all the curl commands we need to download each zim file from all info.json files

        Yields:
            array: commands that can be feeded into subprocess.call()
        """
        for info in self.info_files:
            parser = InfoParser(info)
            url = parser.zimurl()
            file_path = parser.zim_file_path()
            auth = parser.download_auth()
            yield ["curl", "-L", url, "-u", auth, "-o", file_path]
