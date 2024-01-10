# Technical documentation for contributors

## Brand vs app
The name of the brand, is defined as a subfolder.
To clarify things, we have 2 platforms for our apps: iOS and macOS.
Therefore each brand will end up with 2 apps (one for iOS and one for macOS).

## At the beginning we have the following:
- custom brand folders, each with an info.json file, and xcassets
- we have the kiwix/apple code (as a seperate repository). 

    We do not add any swift code to custom apps. All swift code related to custom apps is already included in kiwix/apple repository, it is just "not used" in the Kiwix apps.

The `kiwix/apple` repo is checked out into `/apple` folder, while the custom app repo (this one), is checked out under `/custom` folder.

Since most of the code and files are already in the `/apple` folder, we copy the `/custom` folder under it, so it ends up in: `/apple/custom`. We do the rest of the building from that folder.

## What we need in order to build a custom app?

### A Zim file
This needs to be downloaded from the url given in the `info.json`, and placed under the branded folder, eg: `/custom/dwds`

### A .plist file
The plist file is a list of settings, that is used by xcode for the given target to be built. It is in a required xml format.

It is created under the folder with the same name, eg.: `dwds/dwds.plist`,
with the generated key values such as:
```
APP_STORE_ID = "id6473090365"
CUSTOM_ABOUT_TEXT = "This will be displayed in the about section..."
CUSTOM_ABOUT_WEBSITE = "https://www.dwds.de"
CUSTOM_ZIM_FILE = "dwds_de_dictionary_nopic_2023-12"
SETTINGS_DEFAULT_EXTERNAL_LINK_TO = "alwaysLoad"
SETTINGS_SHOW_SEARCH_SNIPPET = NO
SETTINGS_SHOW_EXTERNAL_LINK_OPTION = NO
```

This way we end up with a plist file dedicated to a specific brand containing all the variables and values it needs.

## Enforced language?
If we use enforcing a language for a brand, what that really means is: we cannot use any of the localization folders contained in the main (kiwix/apple) repo, instead we need to make a copy of a single language folder, eg: `de.lproj` and place it into the custom folder eg: `/custom/dwds/de.lproj` and include only that in the project. 

(Note: only including / excluding does not work as the references to those language folders in the final Xcode project file will mess up. So we need a copy of the folder, and only this way it works as expected.)

An extra step is required here, we also need to set the DEVELOPMENT_LANGUAGE to this value (eg. "de").

# A new custom_project.yml file
The main `kiwix/apple` repo contains a `project.yml` file, it describes all the common build and project settings, and all the templates we re-use to create a final xcode project file, which is used to build the custom apps. At the end each custom app will be a separate target we can build.
Therefore we need dynamically create the `custom_project.yml` file, which will import the `project.yml`, and sets up the new targets (one for each brand), it looks more or less, like this:
```
include:
- project.yml
targets:
  dwds:
    templates:
    - ApplicationTemplate
    settings:
      base:
        DEVELOPMENT_LANGUAGE: de
        INFOPLIST_FILE: custom/dwds/dwds.plist
        INFOPLIST_KEY_CFBundleDisplayName: DWDS
        INFOPLIST_KEY_UILaunchStoryboardName: SplashScreen.storyboard
        MARKETING_VERSION: 2023.12.3
        PRODUCT_BUNDLE_IDENTIFIER: org.kiwix.custom.dwds
    sources:
    - path: custom/dwds
    - path: custom/SplashScreen.storyboard
      destinationFilters:
      - iOS
    - path: Support
      excludes:
      - '*.xcassets'
      - Info.plist
      - '**/*.lproj'
```
Once this is ready, we can call `xcodegen` on it:
```xcodegen -s custom_project.yml``` which will create the `Kiwix.xcodeproj`, and that will contain the original `Kiwix` target and all the branded targets as well eg. `dwds`.

## A splash screen
The splash screen file is going to be the same for each custom app (it is using a branded logo image from the branded xcassets). As you can see from the above example, this file's final location is going to be: `/apple/custom/SplashScreen.storyboard`.
