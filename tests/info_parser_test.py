import unittest
from src.info_parser import InfoParser
from pathlib import Path
import yaml
import os


class InfoParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = InfoParser(Path()/"tests"/"test.json")

    def test_json_to_project_yml(self):
        project = self.parser.as_project_yml()
        print("custom_project.yml targets:")
        print(yaml.dump(project))

    def test_info_plist_path(self):
        custom_info = self.parser._info_plist_path()
        self.assertEqual(custom_info, Path()/"tests"/"tests.plist")

    def test_file_name_from_url(self):
        url = "https://www.dwds.de/kiwix/f/dwds_de_dictionary_nopic_2023-11-20.zim"
        file_name = self.parser._filename_from(url)
        self.assertEqual(file_name, "dwds_de_dictionary_nopic_2023-11-20")

        url = "https://www.dwds.de/kiwix/f/dwds_de_dictionary_nopic_2023-11.zim"
        file_name = self.parser._filename_from(url)
        self.assertEqual(file_name, "dwds_de_dictionary_nopic_2023-11")

    def test_brand_name_from_file_path(self):
        filepath = Path().home()/"some"/"dev"/"path"/"project"/"dwds"/"info.json"
        brand_name = self.parser._brandname_from(filepath)
        self.assertEqual(brand_name, "dwds")

    def test_version_from_filename(self):
        version = self.parser._app_version_from(
            "dwds_de_dictionary_nopic_2023-11-20")
        self.assertEqual(version, "1023.11")

        version = self.parser._app_version_from(
            "dwds_de_dictionary_nopic_2023-09-20")
        self.assertEqual(version, "1023.9")

        version = self.parser._app_version_from(
            "dwds_de_dictionary_nopic_2023-01")
        self.assertEqual(version, "1023.1")

        version = self.parser._app_version_from(
            "dwds_de_dictionary_nopic_2023-12")
        self.assertEqual(version, "1023.12")

    def test_app_name(self):
        app_name = self.parser._app_name()
        self.assertEqual(app_name, "DWDS")

    def test_enforced_language(self):
        enforced_language = self.parser._enforced_language()
        self.assertEqual(enforced_language, "de")

    def test_excluded_languages(self):
        excluded = self.parser._excluded_languages()
        self.assertIn("**/*.lproj", excluded)

    def test_app_version(self):
        self.assertEqual(self.parser._app_version(), "1023.12.3")

    def test_app_version_using_a_tag(self):
        parser = InfoParser(Path()/"tests"/"test.json", build_version=15)
        self.assertEqual(parser._app_version(), "1023.12.15")

        parser = InfoParser(Path()/"tests"/"test.json", build_version=33)
        self.assertEqual(parser._app_version(), "1023.12.33")

    def test_as_plist(self):
        self.parser.create_plist(
            based_on_plist_file=Path()/"tests"/"Support"/"Info.plist")

    def test_zimurl(self):
        self.assertEqual(self.parser.zimurl(
        ), "https://www.dwds.de/kiwix/f/dwds_de_dictionary_nopic_2023-12-15.zim")

    def test_zimfile_path(self):
        self.assertEqual(self.parser.zim_file_path(),
                         Path()/"tests"/"dwds_de_dictionary_nopic_2023-12-15.zim")

    def test_auth_value(self):
        self.assertEqual(self.parser.download_auth(), os.getenv(
            "DWDS_HTTP_BASIC_ACCESS_AUTHENTICATION"))
