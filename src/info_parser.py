#!/usr/bin/env python3

from urllib.parse import urlparse
import json
from pathlib import Path
from version import Version
import os
import shutil
import plistlib

PLIST_KEY_BACKGROUND_MODES = "UIBackgroundModes"
PLIST_KEY_LIVE_ACTIVITY = "NSSupportsLiveActivities"
PLIST_KEY_LIVE_ACTIVITY_FREQUENT = "NSSupportsLiveActivitiesFrequentUpdates"
JSON_KEY_ZIM_URL = "zim_url"
JSON_KEY_AUTH = "zim_auth"
JSON_BUNDLE_ID = "bundle_id"
JSON_KEY_APP_NAME = "app_name"
JSON_KEY_ENFORCED_LANGUAGE = "enforced_lang"
JSON_KEY_DEVELOPMENT_TEAM = "development_team"
JSON_KEY_USES_AUDIO = "uses_audio"
CUSTOM_ZIM_FILE_KEY = "CUSTOM_ZIM_FILE"
JSON_KEY_HIDE_RANDOM_BUTTON = "hide_random_button"
HIDE_RANDOM_BUTTON_KEY = "HIDE_RANDOM_BUTTON"
JSON_TO_PLIST_MAPPING = {
    "app_store_id": "APP_STORE_ID",
    "about_app_url": "CUSTOM_ABOUT_WEBSITE",
    "about_text": "CUSTOM_ABOUT_TEXT",
    "settings_default_external_link_to": "SETTINGS_DEFAULT_EXTERNAL_LINK_TO",
    "settings_show_search_snippet": "SETTINGS_SHOW_SEARCH_SNIPPET",
    "disable_immersive_reading": "DISABLE_IMMERSIVE_READING",
    "settings_show_external_link_option": "SETTINGS_SHOW_EXTERNAL_LINK_OPTION"
}


class InfoParser:

    def __init__(self, json_path, build_number):
        """Parse a specific info.json file for a brand

        Args:
            json_path (Path): of the branded info.json file
            build_number (int, optional): If defined it will be used instead of the info.json[build_number]. Defaults to None.
        """
        self.brand_name = self._brandname_from(json_path)
        content = json_path.read_text()
        self.data = json.loads(content)
        assert (JSON_KEY_ZIM_URL in self.data)
        self.zim_file_name = self._filename_from(
            self.data[JSON_KEY_ZIM_URL])
        self.version = Version.from_file_name(file_name=self.zim_file_name,
                                              build_number=build_number)
        self.development_team_id = self._development_team()
        self.uses_audio = self.data[JSON_KEY_USES_AUDIO] == True

    def create_plist(self, based_on_plist_file):
        with based_on_plist_file.open(mode="rb") as file:
            plist = plistlib.load(file)
            # handle Background mode audio:
            if self.uses_audio == False:
                plist[PLIST_KEY_BACKGROUND_MODES].remove("audio")
            if self._should_hide_random_button():
                plist[HIDE_RANDOM_BUTTON_KEY] = True
            
            # remove live activity for custom apps:
            plist.pop(PLIST_KEY_LIVE_ACTIVITY, None)
            plist.pop(PLIST_KEY_LIVE_ACTIVITY_FREQUENT, None)
            # replace plist values according to custom json:
            for keyValues in self._plist_key_values():
                for key in keyValues:
                    plist[key] = keyValues[key]
            plist[CUSTOM_ZIM_FILE_KEY] = self.zim_file_name
            out_path = self._info_plist_path()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with out_path.open(mode="wb") as out_file:
                plistlib.dump(plist, out_file)

    def as_project_yml(self):
        dict = {
            "templates": ["ApplicationTemplate"],
            "settings": {"base": {
                "MARKETING_VERSION": self.version.semantic, 
                "PRODUCT_BUNDLE_IDENTIFIER": self._bundle_id(),
                "INFOPLIST_FILE": f"custom/{self._info_plist_path()}",
                "INFOPLIST_KEY_CFBundleDisplayName": self._app_name(),
                "INFOPLIST_KEY_UILaunchStoryboardName": "SplashScreen.storyboard",
                "DEVELOPMENT_LANGUAGE": self._dev_language(),
                # without specifying DEVELOPMENT_LANGUAGE,
                # the default value of it: English will be added to the list of
                # selectable languages in iOS Settings,
                # even if the en.lproj is excluded from the sources.
                # If DEVELOPMENT_LANGUAGE is not added, enforcing a single language is not effective,
                # therefore it's better to set it to the enforced language value if there's such.
                "DEVELOPMENT_TEAM": self._development_team()
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
        url = Path(self.zimurl())
        return Path()/self.brand_name/url.name

    def download_auth(self):
        if JSON_KEY_AUTH in self.data:
            auth_key = self.data[JSON_KEY_AUTH]
            return os.getenv(auth_key)
        else:
            return None
        
    def _bundle_id(self):
        if JSON_BUNDLE_ID in self.data:
            return self.data[JSON_BUNDLE_ID]
        else:
            return f"org.kiwix.custom.{self.brand_name}"

    def _info_plist_path(self):
        return Path()/self.brand_name/f"{self.brand_name}.plist"

    def _plist_key_values(self):
        for json_key in JSON_TO_PLIST_MAPPING:
            if json_key in self.data:
                plistKey = JSON_TO_PLIST_MAPPING[json_key]
                value = self.data[json_key]
                yield {plistKey: value}

    def _app_name(self):
        return self.data[JSON_KEY_APP_NAME]
    
    def _development_team(self):
        return self.data[JSON_KEY_DEVELOPMENT_TEAM]

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
        return filepath.parent.name.lower()

    def _filename_from(self, url):
        return Path(urlparse(url).path).stem

    def _excluded_languages(self):
        enforced = self._enforced_language()
        if enforced == None:
            return ["**/qqq.lproj"]
        else:
            # Copy the enforced lang to the custom folder
            for lang_file in Path().cwd().parent.rglob(f'{enforced}.lproj'):
                shutil.copytree(
                    lang_file, Path().cwd().parent/"custom"/self.brand_name, dirs_exist_ok=True)
            # exclude all other languages under Support/*.lproj
            return ["**/*.lproj"]
        
    def _should_hide_random_button(self):
        if JSON_KEY_HIDE_RANDOM_BUTTON in self.data:
            return self.data[JSON_KEY_HIDE_RANDOM_BUTTON] == True
        else:
            return False
