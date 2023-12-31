from glob import glob
from src.info_parser import InfoParser
import os

class CustomApps:

    def __init__(self):
        self.info_files = []
        for f in glob('./**/info.json', recursive=True):
            self.info_files.append(f)
        
    @staticmethod    
    def append_to(custom_plist = "Custom.plist"):
        for cmd in InfoParser.plist_commands():
            os.system("{} {}".format(cmd, custom_plist))
            
    def copy_plist(self, custom_plist):
        for info in self.info_files:
            parser = InfoParser(info)
            os.system("cp {} {}".format(custom_plist, parser.info_plist_path()))

    def create_xcconfigs(self):
        for info in self.info_files:
            parser = InfoParser(info)
            path = "./" + parser.xcconfig_path()
            # create dir, if doesn't exists yet
            dirname = os.path.dirname(path)
            if not os.path.exists(dirname):
                os.makedirs(dirname, exist_ok=True)
            with open(path, 'w') as file:
                file.write(parser.as_xcconfig())
                
    def download_zim_files(self):
        for cmd in self._curl_download_commands():
            os.system(cmd)

    # private                
    def _curl_download_commands(self):
        for info in self.info_files:
            parser = InfoParser(info)
            url = parser.zimurl()
            file_path = parser.zim_file_path()
            auth = parser.download_auth()
            yield "curl -L {} -u {} -o {}".format(url, auth, file_path)
            
            # url=`jq .zim_url -r $info`
            # auth=`jq .zim_auth -r $info`
            
            # parent_url=${url%/*}
            # file_name=${url:${#parent_url} + 1} # + 1 to remove the trailing slash

            # auth_value=`print -rl -- ${(P)auth}` # get the credentials from environment var named by .zim_auth in the json
            # curl -L $url -u "$auth_value" -o $parent_dir/$file_name
