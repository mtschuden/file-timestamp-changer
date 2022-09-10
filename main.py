"""
Created on (Sat) 10.09.2022 11:28:52

@author: Mark Tschuden <mark@tschuden-itsolutions.de>
"""

import json
from os import scandir, path
import os
import sys
from datetime import datetime
import filedate


class File:

    def __init__(self, file):
        self.file = file
        self.path = file.path
        self.timestamp = path.getctime(file.path)
        self.formatted_datetime = datetime.fromtimestamp(
            path.getctime(file.path)
        )

    def __str__(self) -> str:
        return "{} {}".format(self.formatted_datetime, self.file.name)


def filter_by_date(file: File, year=None, month=None, day=None):
    return file.formatted_datetime.year == year


class Backup:

    def __init__(self, dir) -> None:
        self.dir = dir
        self.datetime = datetime.now()
        self.file = "{}_{:02d}_{:02d}T{}{}{}.bak".format(
            self.datetime.year,
            self.datetime.month,
            self.datetime.day,
            self.datetime.hour,
            self.datetime.minute,
            self.datetime.second,
            self.datetime.microsecond
        )
        self.changes = []

    def change(self, file: File, new: float):
        self.changes.append(
            {
                'file': file.path,
                'old': file.timestamp,
                'new': new
            }
        )

    def backup(self):
        with open(self.dir + os.sep + self.file, 'a') as file:
            for change in self.changes:
                file.write(json.dumps(change) + "\n")
            file.close()


def main(dir: str):

    to_replace_year = 2016
    new_year = 2022

    backup = Backup(dir)
    files = [File(file) for file in scandir(dir) if file.is_file()]
    files.sort(key=lambda f: f.timestamp)
    files = filter(lambda f: filter_by_date(f, year=to_replace_year), files)
    for file in files:
        new_datetime = file.formatted_datetime.replace(year=new_year)
        filedate.File(file.file.path).set(
            created=new_datetime,
            modified=new_datetime
        )
        backup.change(file, new_datetime.timestamp())

    backup.backup()


if __name__ == "__main__":
    arg = sys.argv[1]
    if arg == "":
        print("Please specify a directory.")
    main(arg)
