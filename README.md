# Kiwix Apple Custom Apps

Kiwix Apple custom apps are iOS/macOS apps running [Kiwix for
Apple](https://github.com/kiwix/apple) against a
pre-configured ZIM file.

This project contains data and scripts needed to create specific
 custom Kiwix Apple apps.

[![CodeFactor](https://www.codefactor.io/repository/github/kiwix/kiwix-apple-custom/badge)](https://www.codefactor.io/repository/github/kiwix/kiwix-apple-custom)
[![CI Build Status](https://github.com/kiwix/kiwix-apple-custom/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/kiwix/apple/actions/workflows/ci.yml?query=branch%3Amain)
[![CD Build Status](https://github.com/kiwix/kiwix-apple-custom/actions/workflows/cd.yml/badge.svg?branch=main)](https://github.com/kiwix/kiwix-apple-custom/actions/workflows/cd?query=branch%3Amain)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Custom app folder

[In the repository](https://github.com/kiwix/kiwix-apple-custom),
each custom configuration is isolated in a so called custom app
folder. If you need to create a new one for a new custom app, please use a folder name
that is lowercased and contains no space.

## `info.json` file

The configuration of the custom app is handled using the `info.json`
file which **is required to be placed in the custom app folder**. Take example on an already
existing one if you need to create a new custom app. The most
important fields are:
- `about_app_url` - this is an external link that is placed in the "About section" of the application. (Eg. "https://www.dwds.de")
- `about_text` - this is a custom text that is placed in the "About section" describing what the application is about.
- `app_name` - the title of the app
- `app_store_id` - this should to be taken from the developer.apple.com, where the application release is prepared. Note you can use the app_store_id even if the app is not yet released. The id is used within the app in the "Rate the app" section, so users can be redirected to a specific app in the App Store, to rate it.
- `build_version` - it should be a single digit number, used as the last part of the final app version.
[MAJOR].[MINOR].**[PATCH]**. The final version of the app contains the date of the ZIM file provided (using the year and month) and the build_version as the last part. The format of the version comes from the [Apple docs](https://developer.apple.com/documentation/bundleresources/information_property_list/cfbundleshortversionstring). Eg., given a ZIM file: "dictionary_nopic_2023-12-15.zim", and "build_version": "5" we combine it the following way: take the year 2023 and the month 12 from the ZIM file, and combine it with the build_version, resulting in: "2023.12.5". [More on this process here](https://github.com/kiwix/apple/issues/559).
- `enforced_lang` - (lang code eg: en, de, he) if it is set, it will include only this language in the final app, meaning no other languages can be selected (on iOS) for the application UI. See the current list of supported languages [already translated in the main repo](https://github.com/kiwix/apple/tree/main/Support). When using this option, make sure that [the translation coverage](https://translatewiki.net/wiki/Special:MessageGroupStats/kiwix-apple?group=kiwix-apple&messages=&suppressempty=1&x=D) is 100% for the enforced language.
 
    If enforced_lang is not added to the info.json file, all languages will be supported by the app, just like in Kiwix.

- `settings_default_external_link_to` - this controls how external links (pointing to content on the web, that are not included in the zimfile) should be treated. It can take one of the following values: 
    - **"alwaysLoad"**: meaning it will leave the app, and open the link in the system browser, without asking
    - **"alwaysAsk"**: it will ask the user in a pop-up, before opening any external links
    - **"neverLoad"**: it won't ask the user, and won't open any external links. This is handy  if the external links handling is already contained in the zimfile itself, and we don't want to trigger any system level behaviour.
- `settings_show_external_link_option` - **true/false** in the app settings, the user is allowed to change the external link handling behaviour. If we want to restrict that and remove this option from the settings UI (so that the user cannot change the value), we can do that  by setting this value to false.
- `settings_show_search_snippet` - in most cases this should be **false** for a custom app. This removes the snippet from the search, which is used to filter the search results by ZIM files in the Kiwix app. Since custom apps come with a single ZIM file, this filter is not needed.
- `zim_url` - this **is required** for a custom app, without this, it is not a custom app at all. This is used in a download step to create the custom app, and then bundled into the app itself. The **filename must end with the date format: YYYY-MM-DD.zim or with: YYYY-MM.zim**, as the version of the app is dictated by this (see above at the `build_version` section).
If your download requires standard http authentication, see `zim_auth`.

    Note: If you see the standard Kiwix like start page after compiling and running your custom app, that's an indication that this value is either missing, or there's something wrong with the zimfile itself.

- `zim_auth` - this is needed if standard http authentication is required to download the ZIM file. This should be set to **an environment variable name**, which will be resolved during build time. Make sure that the environment variable itself is set up properly before running the build process. **Do not place any credentials directly here, it's not safe, and won't work.**

## XCAssets file

Custom app needs a set of images and icons to build properly.
The **filename itself should be named exactly as the custom folder it is in**: Eg: `dwds/dwds.xcassets`
Currently there's no automated way to do this, you can copy an existing set to your folder, rename it and edit the contents in [Xcode](https://developer.apple.com/xcode/):
```
mkdir wikimed
cp -r dwds/dwds.xcassets wikimed/wikimed.xcassets
xed wikimed/wikimed.xcassets
```

These are mostly images and json files underneath, so theoretically they could be edited/replaced without Xcode as well, but the **final results should be verified within the built custom app itself**.

## Versioning the app

The custom app will have a version name displayed in App Store. This version name has to be a date in the format YYYY.MM.build_version, see the `build_version` section above.

License
-------

[GPLv3](https://www.gnu.org/licenses/gpl-3.0) or later, see
[LICENSE](LICENSE) for more details.