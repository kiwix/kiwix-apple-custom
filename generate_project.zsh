#!/bin/zsh

# move the custom files under the same folder as the kiwix repo
mv custom/ apple/
cd apple/custom

# make a custom copy of the Info.plist file
cp ../Support/Info.plist Custom.plist

# download all the zim files, 
# generate all the branded config files, 
# generate the custom project file containing all brands as targets
python "src/generate_and_download.py"

# move the custom project file to the main folder
cp custom_project.yml ../
cd ..
ls -la

# run xcodegen on our custom project
xcodegen -s custom_project.yml