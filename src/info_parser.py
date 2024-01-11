from urllib.parse import urlparse
import json
import os
import re
import shutil
import plistlib
from glob import glob

JSON_KEY_ZIM_URL = "zim_url"
JSON_KEY_AUTH = "zim_auth"
JSON_KEY_APP_NAME = "app_name"
JSON_KEY_ENFORCED_LANGUAGE = "enforced_lang"
CUSTOM_ZIM_FILE_KEY = "CUSTOM_ZIM_FILE"
JSON_TO_PLIST_MAPPING = {
    "app_store_id": "APP_STORE_ID",
    "about_app_url": "CUSTOM_ABOUT_WEBSITE",
    "about_text": "CUSTOM_ABOUT_TEXT",
    "settings_default_external_link_to": "SETTINGS_DEFAULT_EXTERNAL_LINK_TO",
    "settings_show_search_snippet": "SETTINGS_SHOW_SEARCH_SNIPPET",
    "settings_show_external_link_option": "SETTINGS_SHOW_EXTERNAL_LINK_OPTION"
}

class InfoParser:

    def __init__(self, json_path):
        with open(json_path) as file:
            self.brand_name = self._brandname_from(json_path)
            self.data = json.loads(file.read())
            assert (JSON_KEY_ZIM_URL in self.data)
            self.zim_file_name = self._filename_from(
                self.data[JSON_KEY_ZIM_URL])

    def create_plist(self, based_on_plist_file):
        with open(based_on_plist_file, "rb") as file:
            plist = plistlib.load(file)
            for keyValues in self._plist_key_values():
                for key in keyValues:
                    plist[key] = keyValues[key]
            plist[CUSTOM_ZIM_FILE_KEY] = self.zim_file_name
            out_path = self._info_plist_path()
            # create dir, if doesn't exists yet
            dirname = os.path.dirname(out_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname, exist_ok=True)
            with open(out_path, "wb") as out_file:
                plistlib.dump(plist, out_file)

    def as_project_yml(self):
        dict = {
            "templates": ["ApplicationTemplate"],
            "settings": {"base": {
                "MARKETING_VERSION": self._app_version(),
                "PRODUCT_BUNDLE_IDENTIFIER": f"org.kiwix.custom.{self.brand_name}",
                "INFOPLIST_FILE": f"custom/{self._info_plist_path()}",
                "INFOPLIST_KEY_CFBundleDisplayName": self._app_name(),
                "INFOPLIST_KEY_UILaunchStoryboardName": "SplashScreen.storyboard",
                "DEVELOPMENT_LANGUAGE": self._dev_language()
                # without specifying DEVELOPMENT_LANGUAGE,
                # the default value of it: English will be added to the list of
                # selectable languages in iOS Settings,
                # even if the en.lproj is excluded from the sources.
                # If DEVELOPMENT_LANGUAGE is not added, enforcing a single language is not effective,
                # therefore it's better to set it to the enforced language value if there's such.
            }
            },
            "sources": [
                {"path": f"custom/{self.brand_name}"},
                {"path": "custom/SplashScreen.storyboard",
                 "destinationFilters": ["iOS"]
                 },
                {"path": "Support",
                 "excludes": [
                     "*.xcassets",
                     "Info.plist"
                 ] + self._excluded_languages()
                 },
            ]
        }
        return {self.brand_name: dict}

    def zimurl(self):
        return self.data[JSON_KEY_ZIM_URL]

    def zim_file_path(self):
        url = self.zimurl()
        return f"{self.brand_name}/{os.path.basename(url)}"

    def download_auth(self):
        auth_key = self.data[JSON_KEY_AUTH]
        return os.getenv(auth_key)

    def _info_plist_path(self):
        return f"{self.brand_name}/{self.brand_name}.plist"

    def _plist_key_values(self):
        for json_key in JSON_TO_PLIST_MAPPING:
            if json_key in self.data:
                plistKey = JSON_TO_PLIST_MAPPING[json_key]
                value = self.data[json_key]
                yield {plistKey: value}

    def _app_version(self):
        build_version = self.data["build_version"]
        return f"{self._app_version_from(self.zim_file_name)}.{build_version}"

    def _app_name(self):
        return self.data[JSON_KEY_APP_NAME]

    def _dev_language(self):
        enforced = self._enforced_language()
        if enforced == None:
            return "en"
        else:
            return enforced

    def _enforced_language(self):
        if JSON_KEY_ENFORCED_LANGUAGE in self.data:
            return self.data[JSON_KEY_ENFORCED_LANGUAGE]
        else:
            return None

    def _brandname_from(self, filepath):
        return os.path.basename(os.path.dirname(filepath)).lower()

    def _filename_from(self, url):
        return os.path.splitext(os.path.basename(urlparse(url).path))[0]

    def _app_version_from(self, file_name):
        p = re.compile('(?P<year>\d{4})-(?P<month>\d{1,2})')
        m = p.search(file_name)
        year = int(m.group('year'))
        month = int(m.group('month'))
        assert (year > 2000)
        assert (month > 0)
        assert (month <= 12)
        # downgrade the version by 1000 for testing the release
        year -= 1000
        return ".".join([str(year), str(month)])

    def _excluded_languages(self):
        enforced = self._enforced_language()
        if enforced == None:
            return ["**/qqq.lproj"]
        else:
            # Copy the enforced lang to the custom folder
            for lang_file in glob(f'../**/{enforced}.lproj', recursive=True):
                shutil.copytree(
                    lang_file, f"../custom/{self.brand_name}/", dirs_exist_ok=True)
            # exclude all other languages under Support/*.lproj
            return ["**/*.lproj"]
