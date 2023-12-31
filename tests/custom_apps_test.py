import unittest
from src.custom_apps import CustomApps
import os

class CustomAppsTest(unittest.TestCase):
    
    def setUp(self):
        self.custom = CustomApps()
        
    def test_create_xcconfigs(self):
        self.custom.create_xcconfigs()
        
    def test_custom_plist(self):
        os.system('cp ./tests/Support/Info.plist Custom.plist')
        CustomApps.append_to("Custom.plist")
        self.custom.copy_plist("Custom.plist")
        os.system('rm Custom.plist')
        
    def test_custom_project_creation(self):
        self.custom.create_custom_project_file(path="custom_project_test.yml")
        
    def x_test_downloads(self):
        self.custom.download_zim_files()
        
    def x_test_download_commands(self):
        for cmd in self.custom._curl_download_commands():
            print(cmd)