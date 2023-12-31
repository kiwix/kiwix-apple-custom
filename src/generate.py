"""Generate the custom app xcconfig, plist files, and a custom_project.yml. It is searching for info.json files in subfolders, where the subfolder name will become the "brand name" of the custom app."""

import argparse
from custom_apps import CustomApps


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate custom app files by searching for info.json files")
    parser.add_argument(
        '-o', choices=['edit_plist', 'create_xcconfigs', 'copy_plists', 'create_project_yml'])
    return parser.parse_args()


if __name__ == "__main__":
    custom_plist = "Custom.plist"
    arguments = parse_args()
    type = arguments.output
    match type:
        case 'edit_plist':
            CustomApps.append_to(custom_plist)
        case 'create_xcconfigs':
            CustomApps().create_xcconfigs()
        case 'copy_plists':
            CustomApps().copy_plist(custom_plist)
        case 'create_project_yml':
            CustomApps().create_custom_project_file()
