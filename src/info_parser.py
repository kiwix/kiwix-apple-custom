from urllib.parse import urlparse
import json
import os
import re
from glob import glob

JSON_KEY_ZIM_URL = "zim_url"
JSON_KEY_AUTH = "zim_auth"
JSON_KEY_APP_NAME = "app_name"
JSON_KEY_ENFORCED_LANGUAGE = "enforced_lang"
XCCONF_KEY_ZIM_FILE = "CUSTOM_ZIM_FILE"
JSON_TO_XCCONFIG_MAPPING = {
    "about_app_url": "CUSTOM_ABOUT_WEBSITE",
    "about_text": "CUSTOM_ABOUT_TEXT",
    "app_store_id": "APP_STORE_ID",
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

    def as_xcconfig(self):
        xcconfig_dict = {}
        data = self.data
        for json_key in data:
            if json_key in JSON_TO_XCCONFIG_MAPPING:
                xcconfig_dict[JSON_TO_XCCONFIG_MAPPING[json_key]
                              ] = data[json_key]
        xcconfig_dict[XCCONF_KEY_ZIM_FILE] = self.zim_file_name
        return self._format(xcconfig_dict)

    def xcconfig_path(self):
        return "{}/{}.xcconfig".format(self.brand_name, self.brand_name)
    
    def info_plist_path(self):
        return "{}/{}.plist".format(self.brand_name, self.brand_name)

    def as_project_yml(self):
        dict = {
            "templates": ["ApplicationTemplate"],
            "settings": {"base": {
                "MARKETING_VERSION": "{}.{}".format(self._app_version(), self.data["build_version"]),
                "PRODUCT_BUNDLE_IDENTIFIER": "org.kiwix.custom.{}".format(self.brand_name),
                "INFOPLIST_FILE": "custom/{}".format(self.info_plist_path()),
                "INFOPLIST_KEY_CFBundleDisplayName": self._app_name(),
                "INFOPLIST_KEY_UILaunchStoryboardName": "Launch.storyboard"
            }
            },
            "configFiles": {
                "Debug": self._xcconfig_full_path(),
                "Release": self._xcconfig_full_path()
            },
            "sources": [
                {"path": "custom/{}".format(self.brand_name)},
                {"path": "custom/Launch.storyboard",
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
        return "{}/{}".format(self.brand_name, os.path.basename(url))
    
    def download_auth(self):
        auth_key = self.data[JSON_KEY_AUTH]
        return os.getenv(auth_key)

    @staticmethod
    def plist_commands():
        for value in JSON_TO_XCCONFIG_MAPPING.values():
            if value != "APP_STORE_ID":
                yield "/usr/libexec/PlistBuddy -c \"Add :{} string \$({})\"".format(value, value)

    # private

    def _app_version(self):
        return self._app_version_from(self.zim_file_name)

    def _app_name(self):
        return self.data[JSON_KEY_APP_NAME]

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
        return "custom/{}".format(self.xcconfig_path())

    def _app_version_from(self, file_name):
        m = re.search('\d{4}-\d{1,2}', file_name)
        yearMonth = m.group(0)
        (year, month) = map(lambda x: int(x), yearMonth.split("-"))
        assert (year > 2000)
        assert (month > 0)
        assert (month <= 12)
        return ".".join([str(year), str(month)])

    def _excluded_languages(self):
        enforced = self._enforced_language()
        if enforced == None:
            return ["**/qqq.lproj"]
        else:
            excludes = []
            # exclude every lproj folder except the enforced one
            for lang_file in glob('../**/*.lproj', recursive=True):
                if lang_file.endswith("{}.lproj".format(enforced)) == False:
                    file_name = os.path.basename(lang_file)
                    value = "**/{}".format(file_name)
                    excludes.append(value)
            return excludes

    def _format(self, dictionary):
        list = []
        for key in dictionary:
            value = dictionary[key]
            list.append("{} = {}".format(key, value))
        return "\n".join(list)
