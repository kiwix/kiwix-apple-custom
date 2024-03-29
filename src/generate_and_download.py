#!/usr/bin/env python3

"""Generate the custom app plist files, and a custom_project.yml. 
Based on the arguments passed in:  
where the subfolder name will become the "brand name" of the custom app.
"""

from custom_apps import CustomApps
from pathlib import Path


def main():
    brand = Path(".brand_name").read_text()
    build_number = int(Path(".build_number").read_text())

    custom_apps = CustomApps(brands=[brand], build_number=build_number)
    # create the plist files
    custom_apps.create_plists(custom_plist=Path("Custom.plist"))

    # download the zim files
    custom_apps.download_zim_files()

    # finally create the project file, containing all brands as targets
    custom_apps.create_custom_project_file(path=Path("custom_project.yml"))


if __name__ == "__main__":
    main()
