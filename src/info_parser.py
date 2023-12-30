from urllib.parse import urlparse
import json
import os
import re
from glob import glob

JSON_KEY_ZIM_URL = "zim_url"
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
            assert(JSON_KEY_ZIM_URL in self.data)
            self.zim_file_name = self._filename_from(self.data[JSON_KEY_ZIM_URL])

    def as_xcconfig(self):
        xcconfig_dict = {}
        data = self.data
        for json_key in data:
            if json_key in JSON_TO_XCCONFIG_MAPPING:
                xcconfig_dict[JSON_TO_XCCONFIG_MAPPING[json_key]] = data[json_key] 
        xcconfig_dict[XCCONF_KEY_ZIM_FILE] = self.zim_file_name
        return self._format(xcconfig_dict)
    
    def as_project_yml(self):
        dict = {
            "templates": ["ApplicationTemplate"],
            "settings": {"base": {
                "MARKETING_VERSION": "{}.{}".format(self.app_version(), self.data["build_version"]),
                "PRODUCT_BUNDLE_IDENTIFIER": "org.kiwix.custom.{}".format(self.brand_name),
                "INFOPLIST_FILE": "custom/{}/{}.plist".format(self.brand_name, self.brand_name),
                "INFOPLIST_KEY_CFBundleDisplayName": self.app_name(),
                "INFOPLIST_KEY_UILaunchStoryboardName": "Launch.storyboard"
                }
            },
            "configFiles": {
                "Debug": self._xcconfig_path(),
                "Release": self._xcconfig_path()
                },
            "sources": [
                {"path": "custom/{}".format(self.brand_name)},
                {"path": "Support", 
                 "excludes": [
                     "*.xcassets",
                     "Info.plist"
                    ] + self._excluded_languages()
                },
                ]
            }
        return {self.brand_name: dict}
    
    def app_version(self):
        return self._app_version_from(self.zim_file_name)
    
    def app_name(self):
        return self.data[JSON_KEY_APP_NAME]
    
    def enforced_language(self):
        if JSON_KEY_ENFORCED_LANGUAGE in self.data:
            return self.data[JSON_KEY_ENFORCED_LANGUAGE]
        else:
            return None
        
    def _brandname_from(self, filepath):
        return os.path.basename(os.path.dirname(filepath)).lower()
        
    def _filename_from(self, url):
        return os.path.splitext(os.path.basename(urlparse(url).path))[0]
    
    def _xcconfig_path(self):
        return "custom/{}/{}.xcconfig".format(self.brand_name, self.brand_name)
    
    def _app_version_from(self, file_name):
        m = re.search('\d{4}-\d{1,2}', file_name)
        yearMonth = m.group(0)
        (year, month) = map(lambda x: int(x), yearMonth.split("-"))
        assert(year > 2000)
        assert(month > 0)
        assert(month <= 12)
        return ".".join([str(year), str(month)])
    
    def _excluded_languages(self):
        enforced = self.enforced_language()
        if enforced == None:
            return ["**/qqq.lproj"]
        else:
            excludes = []
            #exclude every lproj folder except the enforced one
            for lang_file in glob('./**/*.lproj', recursive=True):
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
            