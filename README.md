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
- `app_store_id` - this should to be taken from the developer.apple.com, where the application release is prepared. Note you can use the app_store_id even if the app is not yet released. You can find this by visiting: https://appstoreconnect.apple.com/apps/, selecting your app, and go to General tab (on the left), and it will be under AppleID. The id is used within the app in the "Rate the app" section, so users can be redirected to a specific app in the App Store, to rate it. it is a sequence of numbers usually, although for the json file we need to append "id" to it. Eg.: "1281693200" becomes "id1281693200".
- `development_team` - this is the development team id used for the build, it can be found in the relevant Apple Development Account (for apps under the Kiwix organisation it will be the same value: L7HWM3SP3L). You can find your team id in the upper right corner of the screen (after you login to) your [Apple Developer Account](https://developer.apple.com/account/resources/certificates/list).
- `enforced_lang` - ISO 639-1 language code (eg: en, de, he) if it is set, it will include only this language in the final app, meaning no other languages can be selected (on iOS) for the application UI. See the current list of supported languages [already translated in the main repo](https://github.com/kiwix/kiwix-apple/tree/main/Support). When using this option, make sure that [the translation coverage](https://translatewiki.net/wiki/Special:MessageGroupStats/kiwix-apple?group=kiwix-apple&messages=&suppressempty=1&x=D) is 100% for the enforced language.

    If enforced_lang is not added to the info.json file, all languages will be supported by the app, just like in Kiwix.

- `settings_default_external_link_to` - this controls how external links (pointing to content on the web, that are not included in the zimfile) should be treated. It can take one of the following values: 
    - **"alwaysLoad"**: meaning it will leave the app, and open the link in the system browser, without asking
    - **"alwaysAsk"**: it will ask the user in a pop-up, before opening any external links
    - **"neverLoad"**: it won't ask the user, and won't open any external links. This is handy  if the external links handling is already contained in the zimfile itself, and we don't want to trigger any system level behaviour.
- `settings_show_external_link_option` - **true/false** in the app settings, the user is allowed to change the external link handling behaviour. If we want to restrict that and remove this option from the settings UI (so that the user cannot change the value), we can do that  by setting this value to false.
- `settings_show_search_snippet` - in most cases this should be **false** for a custom app. This removes the snippet from the search, which is used to filter the search results by ZIM files in the Kiwix app. Since custom apps come with a single ZIM file, this filter is not needed.
- `uses_audio` - (true | false) this will enable or disable the [UIBackgroundModes](https://developer.apple.com/documentation/bundleresources/information-property-list/uibackgroundmodes) audio property in the final .plist file. Please note if the custom app is not using any media playback, it's recommended to turn this off, otherwise the release build might be rejected by Apple with: "The app declares support for audio in the UIBackgroundModes key in your Info.plist but we are unable to locate any features that require persistent audio."
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

Currently the [latest stable release of the Kiwix Apple repository](https://github.com/kiwix/kiwix-apple/releases) is checked out to form a custom app release.
If needed, the development branch of Kiwix can also be used, by adding "_dev" to the release tag, it can be added somewhere at the end of the tag, as all other tag validations (described above) still need to be met, eg: "dwds_2023.12.10_dev_01".

# Release from an external Apple Account (non Kiwix)
In order to use a different Apple Account for your app, further setup is required.

## Creating the App and the Bundle ID for it
First you need to register a bundleID, which is a unique identifier for the app, here:
https://developer.apple.com/account/resources/identifiers/bundleId/add

Apple recommends a reverse domain name, so something like: org.kiwix.app (adjusted to your domain accordingly)

Please leave the "explicit option", and not use a "wildcard one".
For the app itself, please select both iOS and macOS platforms. We support both of those.

The question marks helpfully explain how the values from each input field of the from will be used later on.
You can leave the "full access" turned on, it will allow each team member (of the developer account) to use the app,
so you don't need to invite them one by one (if that's easier for you that is).

Take note of the bundleID you pick for your application, that should be put into info.json (see above).

## TEAM ID:
Take note of your Apple Team ID, this should be also put into the info.json file for your brand. 
The team ID can be found at the bottom of the following page (after signing), under "Membership details":
https://developer.apple.com/account

## Storing secrets in GitHub
A dedicated GitHub environment will be created for your brand, where your secrets will be kept.

> [!NOTE]
> **The values for the below keys contain secret values, do not send them publicly to GitHub tickets, or any publicly available space.** These secrets need to be sent over e-mail or via other Private Message solution.

## Create the development certificate:
You need to create a development certificate for the app here:
https://developer.apple.com/account/resources/certificates/list
- press create a certificate
- select the first option: Apple Development
- press continue (upper right corner)
- Upload a Certificate Signing Request, to create it you need to follow these steps:
https://developer.apple.com/help/account/create-certificates/create-a-certificate-signing-request
    
    > (Note on macOS Sequoia the KeyChain app is not visible by default, but can be found it under: `/System/Library/CoreServices/Applications/Keychain Access.app`, you can create a link to it, that you can add to your `Application` folder. Open Finder, from the top menu select Go -> Go To Folder, copy paste in: "/System/Library/CoreServices/Applications/". To create a link to the "KeyChain Access.app", have it selected and right click on it, and from the hover menu, select: "Make Alias", this will create a link to it on your Desktop. Optionally you can move this link - by draging it - to your Application folder, if you want.)

    For the common name you can use something like: "Kiwix Development" (*adjusted to your app name accordingly)
    Note: You don't need to do the openssl command-line steps here, only the "Keychain Access" ones.
    For convenience, when saving the .certSigningRequest file you can rename it to something like: "Kiwix_Development.certSigningRequest".

    Once it's approved, you should download your .cer file to your computer, and keep it safe (also you can rename the .cer file to something more meaningful eg: Kiwix_Development.cer).

    You can go back to: "All certificates"

## Create a distribution certificate:

Similarly to the former step, start here:
https://developer.apple.com/account/resources/certificates/list
- press create a certificate
- select the second option: Apple Distribution
- again you need to create a new Certificate Signing Request (a seperate one), following the same steps (see above):
https://developer.apple.com/help/account/create-certificates/create-a-certificate-signing-request

For the common name you can use something like: "Kiwix Distribution" (*adjusted to your app name accordingly)
And as above you can rename the files in this process accrodingly eg to: "Kiwix_Distribution.certSigningRequest", and "Kiwix_Distribution.cer"

## Export the above certificates to .p12 files. 
By opening those .cer files on your mac (both Kiwix_Development.cer and Kiwix_Distribution.cer), they will be added to your system keychain, and they will appear in the Keychain App (see above). For each of those - in the Keychain App - you should right click on the certificate, and select "Export ...", and leave the file format on .p12.
In the export process, you need to choose a password for the exported item (you can use password assistant, by clicking on the key icon). 
Please take a note of these password for both certificates (it is recommended to have a different pass for development and distribution).
(In the end, the export process will ask for your system user password as well to finish this process.)

The content of the .p12 files and the associated passwords, should be added to GitHub Secrets, under the following keys:
- APPLE_DEVELOPMENT_SIGNING_CERTIFICATE
- APPLE_DEVELOPMENT_SIGNING_P12_PASSWORD
- APPLE_DISTRIBUTION_SIGNING_CERTIFICATE
- APPLE_DISTRIBUTION_SIGNING_P12_PASSWORD

## Creating an App Store Connect API Key

- Create a new App Store Connect API Key in the [Users and Access page](https://appstoreconnect.apple.com/access/users)

    - For more info, go to the [App Store Connect API Docs](https://developer.apple.com/documentation/appstoreconnectapi/creating_api_keys_for_app_store_connect_api)

    - Open the `Integrations` tab, select `App Store Connect API`, and create a new "Team Key" using the + button
    - Note that if you can't see the App Store Connect API tab, this means you don't have permission yet. Please refer to the docs above to know how to get this permission

    - Give your API Key an appropriate role (Account Holder) for the task at hand. You can read more about roles in [Permissions in App Store Connect](https://developer.apple.com/support/roles/)

    - Note the Issuer ID as you will need it for the configuration steps below

- Download the newly created API Key file (.p8)
    - This file cannot be downloaded again after the page has been refreshed

From this step you will have the values for the following GitHub secret keys:

- APPLE_STORE_AUTH_KEY
- APPLE_STORE_AUTH_KEY_ID
- APPLE_STORE_AUTH_KEY_ISSUER_ID

## Add test devices 
In order to test the app, and in order to even upload it to TestFlight, physical devices needs to be registered on the Apple Developer Account.
It can be done either via XCode, or via the AppStore Connect, as described here:
https://developer.apple.com/help/account/register-devices/register-a-single-device/

## Create a provisioning profile
Uploading builds to TestFlight requires at least one provision profile to be added. 
It should contain the development certificate created 
earlier (see above), and should also include the test devices (see above).
Here is the detailed Apple documentation on how to create a new development provisitioning profile:
https://developer.apple.com/help/account/manage-provisioning-profiles/create-a-development-provisioning-profile

## Create a Development Signing Identity (optional)

If you whish to have the macOS application distributed outside of the AppStore, it needs to be signed with yet another type of certificate, called Developer Signing Identity.
It can be obtained from App Store Connect with an Account Holder Account here:
    https://developer.apple.com/account/resources/certificates/add

Select `Developer ID Application` and proceed.
    
Once you have the certificate file, it should be exported into a .p12 format, as above (Export those certificates as .p12 files.)

These will be stored under Github Secrets:
- APPLE_DEVELOPER_ID_SIGNING_CERTIFICATE
- APPLE_DEVELOPER_ID_SIGNING_P12_PASSWORD

## Create an app-specific password for notary tool (optional)

If you whish to have the macOS application distributed outside of the AppStore, it needs to verified by Apple, in a process called notarization. For this to happen, you need to provide your App Store Connect credentials (the you use to sign into developer.apple.com). Instead of giving away your very own user name and password, you can create an app-specific password for the notary tool, as described here:
https://support.apple.com/en-us/102654

These also goes to GitHub Secrets:
- APPLE_SIGNING_ALTOOL_USERNAME
- APPLE_SIGNING_ALTOOL_PASSWORD

## ZIM file behind http authentication (optional)
- HTTP_BASIC_ACCESS_AUTHENTICATION - (optional) this is the http basic authentication username:password, it is required to be set if the ZIM file to be downloaded during automated build is behind authentication. This is using the format: "my_user:secret_password".

License
-------

[GPLv3](https://www.gnu.org/licenses/gpl-3.0) or later, see
[LICENSE](LICENSE) for more details.
