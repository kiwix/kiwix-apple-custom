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
        
    def x_test_downloads(self):
        self.custom.download_zim_files()
        
    def x_test_download_commands(self):
        for cmd in self.custom._curl_download_commands():
            print(cmd)