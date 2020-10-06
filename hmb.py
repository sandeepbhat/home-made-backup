# MIT License

# Copyright (c) 2020 Sandeep Bhat

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Create an archive with the folders given in the list for the purpose of backing up."""

import pathlib
import tarfile
import datetime
import argparse
import json


class ConfigParser():
    """Configuration file parser."""
    def __init__(self, config_file_name: str):
        """Intialization."""
        self._config_file = config_file_name
        self._config = dict()

    def parse(self) -> bool:
        """Parse the given config file."""
        config_file_path = pathlib.Path(self._config_file)
        if not config_file_path.exists():
            return False
        with open(str(config_file_path), "r") as fhandle:
            self._config = json.load(fhandle)
        return True

    def get_config(self, config_name: str):
        """Given a config name return it's value."""
        return self._config[config_name]


def create_backup(config_file: str) -> bool:
    """Create a backup with inputs from config file."""
    # Create config parser instance
    config_parser = ConfigParser(config_file)

    # Parse the config file
    if not config_parser.parse():
        print("Error parsing configuration")
        return False

    # 1. Generate backup archive file name
    # Determine archive extension
    extension = config_parser.get_config("archive_type")

    # zip not supported
    if extension == "zip":
        print("zip archiving is not supported. Update the configuration to use tar.*")
        return False

    # Archive open mode is determined by extension
    mode = "w:{}".format(extension)

    extension = "tar.{}".format(extension)

    # Current time in HourMinSeconds_YearMonthDay format
    time_now = datetime.datetime.now().strftime("%H%M%S_%Y%m%d")

    # Get file name prefix
    prefix = config_parser.get_config("archive_prefix")

    # Finally assemble the archive file name
    filename = "{}_{}.{}".format(prefix, time_now, extension)

    # Create destination dir if does not exist
    destdir = pathlib.Path(config_parser.get_config("archive_destination"))
    if not destdir.exists():
        destdir.mkdir()

    output_file = pathlib.Path(destdir, filename)

    # 2. Create the archive
    # Create the backup archive file on disk.
    with tarfile.open(str(output_file), mode=mode) as backup:
        # 3. Go through the list of items which need to be backed up
        for item in config_parser.get_config("items"):
            item_path = pathlib.Path(item)
            # Add it to the archive if the file exists
            if item_path.exists():
                backup.add(str(item_path))
                print("{} added to {}".format(str(item_path), output_file))
            else:
                print("{} does not exist".format(str(item_path)))

    return True


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Home made backup solution")
    parser.add_argument(
        "-i", "--config", dest="config_file", required=True, help="Path to configuration file")
    return parser.parse_args()


if __name__ == "__main__":
    options = parse_args()
    create_backup(options.config_file)
