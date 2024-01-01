"""
The MIT License (MIT)

Copyright (c) 2023-present AbstractUmbra

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import json
import os
import pathlib
import platform
from typing import Any, Literal

__all__ = (
    "_to_json",
    "_from_json",
    "MISSING",
    "SaveValue",
    "resolve_save_path",
)

SaveValue = Literal[1, 2, 3, "1", "2", "3"]

try:
    import orjson
except ModuleNotFoundError:

    def _to_json(obj: Any, /) -> str:
        """A quick method that dumps a Python type to JSON object."""
        return json.dumps(obj, separators=(",", ":"), ensure_ascii=True, indent=2, sort_keys=True)

    _from_json = json.loads  # type: ignore # the overloads are too much for our use case.
else:

    def _to_json(obj: Any, /) -> str:
        """A quick method that dumps a Python type to JSON object."""
        return orjson.dumps(obj, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS).decode("utf-8")

    _from_json = orjson.loads  # type: ignore # this is guarded in an if.


class _MissingSentinel:
    __slots__ = ()

    def __eq__(self, other: object) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self) -> str:
        return "..."


MISSING: Any = _MissingSentinel()


def resolve_save_path(save_number: SaveValue, /) -> pathlib.Path:
    if platform.system() != "Windows":
        raise NotImplementedError("Currently we don't support non-Windows yet.")

    user_profile = os.getenv("USERPROFILE")
    if not user_profile:
        raise RuntimeError("This shouldn't happen or your windows profile is messed up.")

    save_data_path = pathlib.Path(user_profile) / "AppData" / "LocalLow" / "ZeekerssRBLX" / "Lethal Company"

    save_file_name = f"LCSaveFile{save_number}"

    return save_data_path / save_file_name
