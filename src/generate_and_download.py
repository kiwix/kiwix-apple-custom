"""Generate the custom app xcconfig, plist files, and a custom_project.yml. It is searching for info.json files in subfolders, where the subfolder name will become the "brand name" of the custom app."""

from custom_apps import CustomApps

if __name__ == "__main__":
    custom_plist = "Custom.plist"
    custom_apps = CustomApps()
    
    # first edit the plist file
    custom_apps.append_to(custom_plist)
    
    # then copy it to the brand folders
    custom_apps.copy_plist(custom_plist)
    
    # create the xcconfig files
    custom_apps.create_xcconfigs()
    
    # download the zim files
    custom_apps.download_zim_files()
    
    # finally create the project file, containing all brands as targets
    custom_apps.create_custom_project_file()
