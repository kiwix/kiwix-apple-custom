"""Parse a given info.json file and output the content as xcconfig || app_version || app_name."""

import argparse
import os
from info_parser import InfoParser

class NotAnInfoFileError(BaseException):
    """Not an info.json file"""

def info_file_type(string):
    if os.path.exists(string):
        if os.path.basename(string) == "info.json":
            return string
        else:
            raise NotAnInfoFileError(string)    
    else:
        raise FileNotFoundError(string)
        

def parse_args():
    parser = argparse.ArgumentParser(description="Generate xcconfig file content from an info.json file")
    parser.add_argument('info_file', type=info_file_type)
    parser.add_argument('--output', choices=['xcconfig', 'app_version', 'app_name'], default='xcconfig')
    return parser.parse_args()

if __name__ == "__main__":
    arguments = parse_args()
    type = arguments.output
    parser = InfoParser(arguments.info_file)
    match type:
        case 'xcconfig':
            print(parser.as_xcconfig())
        case 'app_version':
            print(parser.app_version())
        case 'app_name':
            print(parser.app_name())
    
    