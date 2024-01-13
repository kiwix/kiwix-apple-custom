"""Generate the custom app plist files, and a custom_project.yml. 
Based on the arguments passed in:  
where the subfolder name will become the "brand name" of the custom app.
"""

from custom_apps import CustomApps
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Builder of custom apps, based on the passed in (optional) brand name and (optional) build version")
    parser.add_argument(
        "brand_name",
        nargs='?',
        default='all',
        help="The brand name to be built, if not provided will fall back to all apps",
        type=str
    )

    parser.add_argument(
        "build_number",
        nargs='?',
        default=None,
        help="The optional build version to use, if not provided will fall back to the build_number defined in the info.json value",
        type=int
    )
    args = parser.parse_args()
    brand = args.brand_name
    build_number = args.build_number

    custom_apps = CustomApps(brands=[brand], build_number=build_number)
    # create the plist files
    custom_apps.create_plists(custom_plist=Path("Custom.plist"))

    # download the zim files
    custom_apps.download_zim_files()

    # finally create the project file, containing all brands as targets
    custom_apps.create_custom_project_file(path=Path("custom_project.yml"))


if __name__ == "__main__":
    main()    