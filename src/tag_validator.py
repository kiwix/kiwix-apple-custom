#!/usr/bin/env python3

import argparse
import re
import sys
from brand import Brand


def _is_valid(tag):
    # Regex verify the tag format
    pattern = re.compile(
        r'^(?P<brand_folder>\w+)_(?P<build_nr>\d+)(?:_(?P<extra_tag>\w+))?$')
    match = pattern.match(tag)

    if match:
        groups = match.groupdict()
        brand_name = groups.get('brand_folder')
        build_nr = int(groups.get('build_nr'))
        brand = Brand(brand_name)
        print(f"{brand.name} {build_nr}")
    else:
        _exit_with_error(f"Invalid tag: {tag}")
        return False


def _exit_with_error(msg):
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
    return _is_valid(args.tag)


if __name__ == "__main__":
    main()
