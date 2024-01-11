#!/usr/bin/env python3

import argparse
import re
from pathlib import Path
import sys


def is_valid(tag):
    # Regex verify the tag format
    pattern = re.compile(
        r'^(?P<brand_folder>\w+)_(?P<build_nr>\d+)(?:_(?P<extra_tag>\w+))?$')
    match = pattern.match(tag)

    if match:
        groups = match.groupdict()
        brand = groups.get('brand_folder')
        build_nr = int(groups.get('build_nr'))
        if Path(brand).is_dir():
            print(f"valid tag found: {tag} (brand: {
                  brand}, build number: {build_nr})")
            return True
        else:
            exist_with_error(f"The directory of the tag: '{
                             brand}' doesn't exist")
    else:
        exist_with_error(f"Invalid tag: {tag}")
        return False


def exist_with_error(msg):
    print(f"Error: {msg}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="A github tag validator for custom apps")
    parser.add_argument(
        "tag",
        help="The github tag to be verified",
        type=str
    )
    args = parser.parse_args()
    return is_valid(args.tag)


if __name__ == "__main__":
    main()
