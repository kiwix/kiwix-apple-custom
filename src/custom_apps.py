from glob import glob
from info_parser import InfoParser
import os
import subprocess
import yaml


class CustomApps:

    def __init__(self):
        self.info_files = []
        for f in glob('./**/info.json', recursive=True):
            self.info_files.append(f)

    def create_custom_project_file(self, path="custom_project.yml"):
        dict = {"include": ["project.yml"]}
        targets = {}
        for info in self.info_files:
            parser = InfoParser(info)
            targets = targets | parser.as_project_yml()

        dict["targets"] = targets
        with open(path, "w") as file:
            yaml.dump(dict, file)

    def create_plists(self, custom_plist):
        for info in self.info_files:
            parser = InfoParser(info)
            parser.create_plist(based_on_plist_file=custom_plist)

    def create_xcconfigs(self):
        for info in self.info_files:
            parser = InfoParser(info)
            path = "./" + parser.xcconfig_path()
            # create dir, if doesn't exists yet
            dirname = os.path.dirname(path)
            if not os.path.exists(dirname):
                os.makedirs(dirname, exist_ok=True)
            with open(path, 'w') as file:
                file.write(parser.as_xcconfig())

    def download_zim_files(self):
        for cmd in self._curl_download_commands():
            subprocess.call(cmd)

    # private
    def _curl_download_commands(self):
        for info in self.info_files:
            parser = InfoParser(info)
            url = parser.zimurl()
            file_path = parser.zim_file_path()
            auth = parser.download_auth()
            yield ["curl", "-L", url, "-u", auth, "-o", file_path]
