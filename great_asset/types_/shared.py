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
