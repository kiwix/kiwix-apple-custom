import unittest
from src.info_parser import InfoParser

class InfoParserTest(unittest.TestCase):
    
    def setUp(self):
        self.parser = InfoParser("tests/test_info.json")
    
    def test_json_to_xcconfig(self):
        xcconfig = self.parser.as_xcconfig()
        print(xcconfig)
        
    def test_file_name_from_url(self):
        url="https://www.dwds.de/kiwix/f/dwds_de_dictionary_nopic_2023-11-20.zim"
        file_name = self.parser._filename_from(url)
        self.assertEqual(file_name, "dwds_de_dictionary_nopic_2023-11-20.zim")
        
    def test_version_from_filename(self):
        version = self.parser._app_version_from("dwds_de_dictionary_nopic_2023-11-20.zim")
        self.assertEqual(version, "2023.11")
        
        version = self.parser._app_version_from("dwds_de_dictionary_nopic_2023-09-20.zim")
        self.assertEqual(version, "2023.9")
        
    def test_app_name(self):
        app_name = self.parser.app_name()
        self.assertEqual(app_name, "DWDS")
        
    def test_app_version(self):
        self.assertEqual(self.parser.app_version(), "2023.11")
        