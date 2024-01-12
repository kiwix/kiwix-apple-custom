from info_parser import InfoParser
from brand import Brand
import subprocess
import yaml

INFO_JSON = 'info.json'

class CustomApps:

    def __init__(self, brands=["all"], build_version=None):
        self.build_version = build_version
        if brands == ["all"]:
            self.info_files = Brand.all_info_files()
        else:
            self.info_files = []
            for brand_name in brands:
                brand = Brand(brand_name)
                self.info_files.append(brand.info_file)

    def create_custom_project_file(self, path):
        """Create the project file based on the main repo project.yml
        It will contain the targets we need for each custom app, and their build settings,
        pointing to their individual info.plist files

        Args:
            path (Path): the output file path where the project yaml will be saved
        """
        dict = {"include": ["project.yml"]}
        targets = {}
        for info in self.info_files:
            parser = InfoParser(info, build_version=self.build_version)
            targets = targets | parser.as_project_yml()

        dict["targets"] = targets
        with open(path, "w") as file:
            yaml.dump(dict, file)

    def create_plists(self, custom_plist):
        """Generate the plist files for each brand

        Args:
            custom_plist (Path): the path to the original plist file we are basing this of,
            it should be a copy from the Kiwix target
        """
        for info in self.info_files:
            parser = InfoParser(info, build_version=self.build_version)
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
            parser = InfoParser(info, build_version=self.build_version)
            url = parser.zimurl()
            file_path = parser.zim_file_path()
            auth = parser.download_auth()
            yield ["curl", "-L", url, "-u", auth, "-o", file_path]
