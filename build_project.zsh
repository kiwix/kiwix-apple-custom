#!/bin/zsh

# move the custom files under the same folder as the kiwix repo
mv custom/ apple/
cd apple/custom

# download custom zim files as per info_local.json files
# and configure the project.yml file accordingly
for info in `python src/find_infos.py`
do
    parent_dir=${info%/*}
    brand_name=${parent_dir##*/}
    echo "brand_name: " $brand_name

    url=`jq .zim_url -r $info`
    auth=`jq .zim_auth -r $info`
    
    parent_url=${url%/*}
    file_name=${url:${#parent_url} + 1} # + 1 to remove the trailing slash

    auth_value=`print -rl -- ${(P)auth}` # get the credentials from environment var named by .zim_auth in the json
    curl -L $url -u "$auth_value" -o $parent_dir/$file_name

    touch $brand_name/$brand_name.xcconfig
    python src/configure.py --output xcconfig $info > $brand_name/$brand_name.xcconfig
    echo "app name"
    python src/configure.py --output app_name $info
    echo "app version"
    python src/configure.py --output app_version $info
    echo "enforced language"
    python src/configure.py --output enforced_language $info

    # copy the Info.plist file to custom folder
    cp ../Support/Info.plist $brand_name/$brand_name.plist

    # TODO: do this only once as Custom.plist, then just copy to the $brand folder as above
    /usr/libexec/PlistBuddy -c "Add :CUSTOM_ZIM_FILE string \$(CUSTOM_ZIM_FILE)" $brand_name/$brand_name.plist
    /usr/libexec/PlistBuddy -c "Add :CUSTOM_ABOUT_TEXT string \$(CUSTOM_ABOUT_TEXT)" $brand_name/$brand_name.plist
    /usr/libexec/PlistBuddy -c "Add :CUSTOM_ABOUT_WEBSITE string \$(CUSTOM_ABOUT_WEBSITE)" $brand_name/$brand_name.plist
    /usr/libexec/PlistBuddy -c "Add :SETTINGS_DEFAULT_EXTERNAL_LINK_TO string \$(SETTINGS_DEFAULT_EXTERNAL_LINK_TO)" $brand_name/$brand_name.plist
    /usr/libexec/PlistBuddy -c "Add :SETTINGS_SHOW_EXTERNAL_LINK_OPTION string \$(SETTINGS_SHOW_EXTERNAL_LINK_OPTION)" $brand_name/$brand_name.plist
    /usr/libexec/PlistBuddy -c "Add :SETTINGS_SHOW_SEARCH_SNIPPET string \$(SETTINGS_SHOW_SEARCH_SNIPPET)" $brand_name/$brand_name.plist
done

cd ..
ls -la

# run xcodegen on our custom project:
xcodegen -s custom_project.yml