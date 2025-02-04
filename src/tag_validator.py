#!/usr/bin/env python3

import argparse
import re
import sys
from brand import Brand
from version import Version
from info_parser import InfoParser
from pathlib import Path


def _is_valid(tag):
    # Regex verify the tag format: folder_YYYY.MM.buildNr(_extra)
    pattern = re.compile(
        r'^(?P<brand_name>\w+)_(?P<year>\d{4})\.(?P<month>\d{1,2})\.(?P<build_number>\d+)(?:_(?P<extra_tag>\w+))?$'
    )
    match = pattern.match(tag)

    if match:
        groups = match.groupdict()
        brand_name = groups.get('brand_name')
        year = int(groups.get('year'))
        month = int(groups.get('month'))
        build_number = int(groups.get('build_number'))
        
        try:
            brand = Brand(brand_name)
        except FileExistsError as e:
            _exit_with_error(f"Invalid tag {tag}: {e}")
            
        try:
            version = Version(
                year=year, month=month, build_number=build_number
            )
        except ValueError as e:
            _exit_with_error(f"Invalid tag {tag}: {e}")
            
        parser = InfoParser(json_path=brand.info_file, build_number=version.build_number)
        if parser.version != version:
            _exit_with_error(f"Invalid date in tag: {tag}, does not match year.month of ZIM file in {brand.info_file}, it should be: {parser.version.semantic}")
        
        # save the specific parts of the tag as temp files:
        Path('.brand_name').write_text(f"{brand.name}")
        Path('.build_number').write_text(f"{version.build_number}")
        Path('.version_number').write_text(f"{version.semantic}")
        Path('.team_id').write_text(f"{parser.development_team_id}")
        
        # required as an output, we can pipe on:
        print(f"{brand.name} {version.build_number}")
        
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
