import unittest
from src.custom_apps import CustomApps
from pathlib import Path


class CustomAppsTest(unittest.TestCase):

    def setUp(self):
        self.custom = CustomApps()

    def test_custom_plist(self):
        self.custom.create_plists(
            custom_plist=Path()/"tests"/"Support"/"Info.plist")

    def test_custom_project_creation(self):
        self.custom.create_custom_project_file(path=Path()/"custom_project_test.yml")

    def x_test_downloads(self):
        self.custom.download_zim_files()

    def x_test_download_commands(self):
        for cmd in self.custom._curl_download_commands():
            print(cmd)
