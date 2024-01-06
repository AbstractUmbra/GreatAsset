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
from __future__ import annotations

from random import choice, uniform
from typing import TYPE_CHECKING

TOP_SHELF = 2.5
UPPER_SHELF = 2.0
LOWER_SHELF = 1.5
BOTTOM_SHELF = 1.0
SHELVES = [TOP_SHELF, UPPER_SHELF, LOWER_SHELF, BOTTOM_SHELF]

if TYPE_CHECKING:
    from .types_.save_file import InnerVectorValue

__all__ = ("Vector",)


class Vector:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x: float = float(x)
        self.y: float = float(y)
        self.z: float = float(z)

    def __repr__(self) -> str:
        return f"<Vector x={self.x} y={self.y} z={self.z}>"

    @classmethod
    def default(cls) -> Vector:
        return cls(-3.5, 2.5, -12.5)

    @classmethod
    def on_cupboard(cls) -> Vector:
        return cls(uniform(2.5, 3.5), choice(SHELVES), uniform(-12, -12.5))

    @classmethod
    def from_dict(cls, payload: InnerVectorValue) -> Vector:
        return cls(**payload)

    def serialise(self) -> InnerVectorValue:
        return {"x": self.x, "y": self.y, "z": self.z}
