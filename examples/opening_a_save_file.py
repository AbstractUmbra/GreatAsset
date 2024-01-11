"""
This example outlines the ways we can open a save file and utilise them.
"""

import pathlib

from great_asset import SaveFile


def raw_bytes() -> None:
    """
    This method utilises Python's native ability to open files for binary reading.
    """
    with open("/path/to/save", "rb") as fp:  # noqa: PTH123
        data = fp.read()

    save = SaveFile(data)

    print(save.credits)


def from_pathlib() -> None:
    """
    This method utilises the builtin pathlib for handling and resolving file paths and locations.
    """
    path = pathlib.Path("/path/to/save")

    save = SaveFile.from_path(path)

    print(save.credits)


def from_path_resolution() -> None:
    """
    This method utilises great_assets utility for loading the default (Windows) save directory and opening the save with the given file number.

    This assumes an unchanged appdata/locallow directory and standard save file naming.
    """
    save = SaveFile.resolve_from_file(1)

    print(save.credits)
