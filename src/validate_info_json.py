#!/usr/bin/env python3

"""Validate the custom app json files passed in as an argument
Making sure we are using https for ZIM the file,
and that it is downloadable
"""

from brand import Brand
import argparse
import info_parser
import json
import requests


def main():
    parser = argparse.ArgumentParser(
        description="Validator for custom apps info.json file")
    parser.add_argument(
        "info_jsons",
        help="The info.json files to be verified",
        type=str,
        nargs="*"
    )
    args = parser.parse_args()
    return _is_valid(args.info_jsons)
    
def _is_valid(info_jsons):
    for info_json in info_jsons:
        with open(info_json, 'r') as info_file:
            content = info_file.read()
            data = json.loads(content)
            zim_url = data[info_parser.JSON_KEY_ZIM_URL]

            # is https
            assert zim_url.startswith(
                "https://"), "ZIM URL is not using https: {}".format(zim_url)

            # try a head request on it
            response = requests.head(zim_url)

            # is reachable
            assert response.status_code in [200, 302], "ZIM URL is not reachable: {} response code: {}".format(
                response.url, response)


if __name__ == "__main__":
    main()
