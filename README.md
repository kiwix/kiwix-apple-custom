# Kiwix Apple Custom Apps

Kiwix Apple custom apps are iOS/macOS apps running [Kiwix for
Apple](https://github.com/kiwix/kiwix-apple) against a
pre-configured ZIM file.

This project contains data and scripts needed to create specific
 custom Kiwix Apple apps.

[![CodeFactor](https://www.codefactor.io/repository/github/kiwix/kiwix-apple-custom/badge)](https://www.codefactor.io/repository/github/kiwix/kiwix-apple-custom)
[![CI Build Status](https://github.com/kiwix/kiwix-apple-custom/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/kiwix/kiwix-apple-custom/actions/workflows/ci.yml)
[![CD Build Status](https://github.com/kiwix/kiwix-apple-custom/actions/workflows/cd.yml/badge.svg?branch=main)](https://github.com/kiwix/kiwix-apple-custom/actions/workflows/cd.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Custom app folder

[In the repository](https://github.com/kiwix/kiwix-apple-custom),
each custom configuration is isolated in a so called custom app
folder. If you need to create a new one for a new custom app, please use a folder name
that is lowercased and contains no space.

## `info.json` file

The configuration of the custom app is handled using the `info.json`
file which **is required to be placed in the custom app folder**. Take example on an already
existing one if you need to create a new custom app.

### The required fields are:
- `about_app_url` - this is an external link that is placed in the "About section" of the application. (Eg. "https://www.dwds.de")
- `about_text` - this is a custom text that is placed in the "About section" describing what the application is about. It is not supporting html tags, but new lines can be added with '\n'.
- `app_name` - Name of the app, as it will appear on device, and in App Store
- `app_store_id` - this should to be taken from the developer.apple.com, where the application release is prepared. Note you can use the app_store_id even if the app is not yet released. The id is used within the app in the "Rate the app" section, so users can be redirected to a specific app in the App Store, to rate it.
- `enforced_lang` - ISO 639-1 language code (eg: en, de, he) if it is set, it will include only this language in the final app, meaning no other languages can be selected (on iOS) for the application UI. See the current list of supported languages [already translated in the main repo](https://github.com/kiwix/kiwix-apple/tree/main/Support). When using this option, make sure that [the translation coverage](https://translatewiki.net/wiki/Special:MessageGroupStats/kiwix-apple?group=kiwix-apple&messages=&suppressempty=1&x=D) is 100% for the enforced language.

    If enforced_lang is not added to the info.json file, all languages will be supported by the app, just like in Kiwix.

- `settings_default_external_link_to` - this controls how external links (pointing to content on the web, that are not included in the zimfile) should be treated. It can take one of the following values: 
    - **"alwaysLoad"**: meaning it will leave the app, and open the link in the system browser, without asking
    - **"alwaysAsk"**: it will ask the user in a pop-up, before opening any external links
    - **"neverLoad"**: it won't ask the user, and won't open any external links. This is handy  if the external links handling is already contained in the zimfile itself, and we don't want to trigger any system level behaviour.
- `settings_show_external_link_option` - **true/false** in the app settings, the user is allowed to change the external link handling behaviour. If we want to restrict that and remove this option from the settings UI (so that the user cannot change the value), we can do that  by setting this value to false.
- `settings_show_search_snippet` - in most cases this should be **false** for a custom app. This removes the snippet from the search, which is used to filter the search results by ZIM files in the Kiwix app. Since custom apps come with a single ZIM file, this filter is not needed.
- `zim_url` - this **is required** for a custom app, without this, it is not a custom app at all. This is used in a download step to create the custom app, and then bundled into the app itself. The **filename must end with the date format: YYYY-MM-DD.zim or with: YYYY-MM.zim**, as the version of the app is dictated by this. See more on that in the "Versioning and creating the app" section below.
If your download requires standard http authentication, see `zim_auth`.

    Note: If you see the standard Kiwix like start page after compiling and running your custom app, that's an indication that this value is either missing, or there's something wrong with the zimfile itself.

### Optional fields

These key / values can be, but do not need to be included in the `info.json` file:

- `bundle_id` - (optional) It should match to the bundle id set on the Apple Developer website for this app. If it's not set it will default to: "org.kiwix.custom.{brand_name}", where the brand name is the name of the folder, eg: "org.kiwix.custom.dwds".

- `zim_auth` - (optional) this is needed if standard http authentication is required to download the ZIM file. This should be set to **an environment variable name**, which will be resolved during build time. Make sure that the environment variable itself is set up properly before running the build process. **Do not place any credentials directly here, it's not safe, and won't work.**

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

# Versioning and releasing

**In short: the app version is dictated by Github release tags.**

The release process ensures a systematic and clear versioning and releasing workflow for custom apps. You need to use GitHub release tags to trigger TestFlight uploads. The automated process guarantees compliance with [our versioning rules](https://github.com/kiwix/kiwix-apple/issues/559) and [Apple's versioning guidelines](https://developer.apple.com/documentation/bundleresources/information_property_list/cfbundleshortversionstring).

The app version must be in the format: `YYYY.MM.build_version` [More on this process here](https://github.com/kiwix/kiwix-apple/issues/559), this version will be visible in the App Store.

Each release is tied to a Github release tag. The tag can be defined when creating the release. The name of the tag is going to determine which app we want to release, and what the final version of that app will be.
The tag naming must follow the format:
`{brand_name}_YYYY.MM.{build_number}(_optional-part)`, eg: `dwds_2023.12.9` or `wikimed_2023.12.88_test`)

Where the:
- `brand_name` is the name of the brand, an existing folder in the repository (eg: "dwds", or "wikimed"). It needs to be lowercase and the folder must exist and must contain an `info.json` file. It is validated, and in case of a mistake the release process will stop with an invalid tag error.
- `YYYY.MM` is a date matching the ZIM file's date in the `info.json` file defined under `zim_url`. See above. It is also validated, and in case of a mistake the process will stop with an invalid tag error.
- `build_number` - it must be a non-negative integer (0 and above), incrementing for the same ZIM file, eg: `dwds_2023.12.9` => `dwds_2023.12.10` This allows to create different app versions with the same ZIM file. If a new ZIM file is used (compared to former version, or it's the first release of a new app), it should be `0`, eg: `dwds_2027.01.0` or `brandnewapp_2024.10.0`.
- `optional-part` - any value can be added here, it is only indicative, eg for different attempts to release the same app version, such as in the case of a failed build restart, eg: `dwds_2023.12.90_testing01`, `dwds_2023.12.90_testing02`. The value of the optional part is ignored in the build process, it is only an indicator, we can use to distinguish between attempts to release the very same version of an app.

Note: Both iOS and macOS applications are created from the same source code and are versioned and released together.

License
-------

[GPLv3](https://www.gnu.org/licenses/gpl-3.0) or later, see
[LICENSE](LICENSE) for more details.
