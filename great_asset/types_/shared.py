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

from typing import Literal, TypedDict

__all__ = (
    "StringValue",
    "IntValue",
    "FloatValue",
    "BoolValue",
    "ArrayIntValue",
    "InnerVectorValue",
    "VectorValue",
    "ArrayVectorValue",
)


class StringValue(TypedDict):
    __type: Literal["string"]
    value: str


class IntValue(TypedDict):
    __type: Literal["int"]
    value: int


class FloatValue(TypedDict):
    __type: Literal["float"]
    value: float


class BoolValue(TypedDict):
    __type: Literal["bool"]
    value: bool


class ArrayIntValue(TypedDict):
    __type: Literal["System.Int32[],mscorlib"]
    value: list[int]


class InnerVectorValue(TypedDict):
    x: float
    y: float
    z: float


class VectorValue(TypedDict):
    __type: Literal["Vector3"]
    value: InnerVectorValue


class ArrayVectorValue(TypedDict):
    __type: Literal["UnityEngine.Vector3[],UnityEngine.CoreModule"]
    value: list[InnerVectorValue]
