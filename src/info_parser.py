from urllib.parse import urlparse
import json
import os
import re
import shutil
from glob import glob

JSON_KEY_ZIM_URL = "zim_url"
JSON_KEY_AUTH = "zim_auth"
JSON_KEY_APP_NAME = "app_name"
JSON_KEY_ENFORCED_LANGUAGE = "enforced_lang"
XCCONF_KEY_ZIM_FILE = "CUSTOM_ZIM_FILE"
JSON_TO_PLIST_MAPPING = {
    "about_app_url": {"CUSTOM_ABOUT_WEBSITE": "string"}
}
JSON_TO_XCCONFIG_MAPPING = {
    "about_text": {"CUSTOM_ABOUT_TEXT": "string"},
    "app_store_id": {"APP_STORE_ID": "string"},
    "settings_default_external_link_to": {"SETTINGS_DEFAULT_EXTERNAL_LINK_TO": "string"},
    "settings_show_search_snippet": {"SETTINGS_SHOW_SEARCH_SNIPPET": "bool"},
    "settings_show_external_link_option": {"SETTINGS_SHOW_EXTERNAL_LINK_OPTION": "bool"}
}


class InfoParser:

    def __init__(self, json_path):
        with open(json_path) as file:
            self.brand_name = self._brandname_from(json_path)
            self.data = json.loads(file.read())
            assert (JSON_KEY_ZIM_URL in self.data)
            self.zim_file_name = self._filename_from(
                self.data[JSON_KEY_ZIM_URL])

    def as_xcconfig(self):
        xcconfig_dict = {}
        data = self.data
        for json_key in data:
            if json_key in JSON_TO_XCCONFIG_MAPPING:
                xcconfig_dict[next(iter(JSON_TO_XCCONFIG_MAPPING[json_key]))
                              ] = data[json_key]
        xcconfig_dict[XCCONF_KEY_ZIM_FILE] = self.zim_file_name
        return self._format(xcconfig_dict)

    def xcconfig_path(self):
        return f"{self.brand_name}/{self.brand_name}.xcconfig"

    def info_plist_path(self):
        return f"{self.brand_name}/{self.brand_name}.plist"

    def as_project_yml(self):
        dict = {
            "templates": ["ApplicationTemplate"],
            "settings": {"base": {
                "MARKETING_VERSION": self._app_version(),
                "PRODUCT_BUNDLE_IDENTIFIER": f"org.kiwix.custom.{self.brand_name}",
                "INFOPLIST_FILE": f"custom/{self.info_plist_path()}",
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
            "configFiles": {
                "Debug": self._xcconfig_full_path(),
                "Release": self._xcconfig_full_path()
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
    
    def append_to_plist_commands(self):
        for jsonKey in JSON_TO_PLIST_MAPPING:
            print(jsonKey)
            if jsonKey in self.data:
                plistObj = JSON_TO_PLIST_MAPPING[jsonKey]
                for plistKey in plistObj:
                    type = plistObj[plistKey]
                    value = self.data[jsonKey]
                    yield InfoParser._add_to_plist_cmd(plistKey, value, type)

    @staticmethod
    def plist_commands():
        for value in (JSON_TO_XCCONFIG_MAPPING.values()):
            for key in value:
                type = value[key]
                if key != "APP_STORE_ID":
                    yield InfoParser._add_var_to_plist_cmd(key, type)
        yield InfoParser._add_var_to_plist_cmd(XCCONF_KEY_ZIM_FILE, "string")

    # private
    @staticmethod
    def _add_var_to_plist_cmd(value, type):
        return InfoParser._add_to_plist_cmd(value, f"\$({value})", type)

    @staticmethod
    def _add_to_plist_cmd(key, value, type):
        return ["/usr/libexec/PlistBuddy", "-c", f"\"Add :{key} {type} {value}\""]
    
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

    def _xcconfig_full_path(self):
        return f"custom/{self.xcconfig_path()}"

    def _app_version_from(self, file_name):
        m = re.search('\d{4}-\d{1,2}', file_name)
        yearMonth = m.group(0)
        (year, month) = map(lambda x: int(x), yearMonth.split("-"))
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
                shutil.copytree(lang_file, f"../custom/{self.brand_name}/", dirs_exist_ok=True)
            # exclude all other languages under Support/*.lproj
            return ["**/*.lproj"]

    def _format(self, dictionary):
        list = []
        for key in dictionary:
            value = dictionary[key]
            list.append(f"{key} = {value}")
        return "\n".join(list)
