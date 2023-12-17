#!/bin/zsh

# dependencies
lib_kiwix_framework="libkiwix_xcframework-13.0.0-1"

# move the custom files under the same folder as the kiwix repo
mv custom/ apple/
cd apple

#download custom zim files as per info.json files
brew install jq

for info in `mdfind -onlyin apple/custom/ -name info.json`
do
    parent_dir=${info%/*}
    brand_name=${parent_dir##*/}
    echo "brand_name: " $brand_name

    url=`jq .zim_url -r $info`
    auth=`jq .zim_auth -r $info`
    
    parent_url=${url%/*}
    file_name=${url:${#parent_url} + 1} # + 1 to remove the trailing slash

    auth_value=`print -rl -- ${(P)auth}` # get the credentials from environment var named by .zim_auth in the json
    curl -O -L $url -u "$auth_value" $parent_dir/$file_name

    python src/configure.py --output xcconfig $info > custom/$brand_name/$brand_name.xcconfig
    echo "app name"
    echo python src/configure.py --output app_name $info
    echo "app version"
    echo python src/configure.py --output app_version $info
done

# download libkiwix xcframework
lib_kiwix_url="http://download.kiwix.org/release/libkiwix/"$lib_kiwix_framework".tar.gz"
curl -O -L $lib_kiwix_url
tar xzf $lib_kiwix_framework".tar.gz"
rm $lib_kiwix_framework".tar.gz"
mv libkiwix_xcframework*/lib/*.* .
rm -rf libkiwix_xcframework*/

ls -la

# install xcodegen and run it
brew install xcodegen
xcodegen
