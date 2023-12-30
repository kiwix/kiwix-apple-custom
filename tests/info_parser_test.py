import unittest
from src.info_parser import InfoParser
import yaml

class InfoParserTest(unittest.TestCase):
    
    def setUp(self):
        self.parser = InfoParser("tests/test.json")
    
    def test_json_to_xcconfig(self):
        xcconfig = self.parser.as_xcconfig()
        print(xcconfig)
        
    def test_json_to_project_yml(self):
        project = self.parser.as_project_yml()
        print("custom_project.yml targets:")
        print(yaml.dump(project))
        
    def test_file_name_from_url(self):
        url="https://www.dwds.de/kiwix/f/dwds_de_dictionary_nopic_2023-11-20.zim"
        file_name = self.parser._filename_from(url)
        self.assertEqual(file_name, "dwds_de_dictionary_nopic_2023-11-20")
        
    def test_brand_name_from_file_path(self):
        filepath = "/User/some/dev/path/project/dwds/info.json"
        brand_name = self.parser._brandname_from(filepath)
        self.assertEqual(brand_name, "dwds")
        
    def test_version_from_filename(self):
        version = self.parser._app_version_from("dwds_de_dictionary_nopic_2023-11-20")
        self.assertEqual(version, "2023.11")
        
        version = self.parser._app_version_from("dwds_de_dictionary_nopic_2023-09-20")
        self.assertEqual(version, "2023.9")
        
    def test_app_name(self):
        app_name = self.parser.app_name()
        self.assertEqual(app_name, "DWDS")
        
    def test_enforced_language(self):
        enforced_language = self.parser.enforced_language()
        self.assertEqual(enforced_language, "de")
        
    def test_excluded_languages(self):
        excluded = self.parser._excluded_languages()
        self.assertIn("**/qqq.lproj", excluded)
        self.assertIn("**/ru.lproj", excluded)
        self.assertIn("**/en.lproj", excluded)
        self.assertNotIn("**/de.lproj", excluded)
        
    def test_app_version(self):
        self.assertEqual(self.parser.app_version(), "2023.12")
        