import unittest
from src.version import Version


class VersionTest(unittest.TestCase):

    def test_version_from_filename(self):
        version = Version.from_file_name(
            "dwds_de_dictionary_nopic_2023-11-20", build_number=10)
        self.assertEqual(version.semantic, "2023.11.10")
        self.assertEqual(version.semantic_downgraded, "1023.11.10")

        version = Version.from_file_name(
            "dwds_de_dictionary_nopic_2023-09-20", build_number=0)
        self.assertEqual(version.semantic, "2023.9.0")
        self.assertEqual(version.semantic_downgraded, "1023.9.0")

        version = Version.from_file_name(
            "dwds_de_dictionary_nopic_2023-01", build_number=7)
        self.assertEqual(version.semantic, "2023.1.7")
        self.assertEqual(version.semantic_downgraded, "1023.1.7")

        version = Version.from_file_name(
            "dwds_de_dictionary_nopic_2023-12", build_number=129)
        self.assertEqual(version.semantic, "2023.12.129")
        self.assertEqual(version.semantic_downgraded, "1023.12.129")
