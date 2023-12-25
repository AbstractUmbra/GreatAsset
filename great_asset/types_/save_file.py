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

from typing import Literal, Required, TypedDict

__all__ = ("SaveFile",)


class IntValue(TypedDict):
    __type: Literal["int"]
    value: int


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


SaveFile = TypedDict(
    "SaveFile",
    {
        "CurrentPlanetID": Required[IntValue],
        "DeadlineTime": Required[IntValue],
        "EnemyScans": Required[ArrayIntValue],
        "FileGameVers": Required[IntValue],
        "GroupCredits": Required[IntValue],
        "ProfitQuota": Required[IntValue],
        "QuotaFulfilled": Required[IntValue],
        "QuotasPassed": Required[IntValue],
        "RandomSeed": Required[IntValue],
        "ShipUnlockedMoved_Cupboard": BoolValue,
        "ShipUnlockedMoved_Light switch": BoolValue,
        "ShipUnlockedMoved_Loud horn": BoolValue,
        "ShipUnlockedMoved_Teleporter": BoolValue,
        "ShipUnlockPos_Cupboard": VectorValue,
        "ShipUnlockPos_Light switch": VectorValue,
        "ShipUnlockPos_Loud horn": VectorValue,
        "ShipUnlockPos_Teleporter": VectorValue,
        "ShipUnlockRot_Light switch": VectorValue,
        "ShipUnlockRot_Loud horn": VectorValue,
        "ShipUnlockRot_Teleporter": VectorValue,
        "ShipUnlockStored_Bunkbeds": Required[BoolValue],
        "ShipUnlockStored_Cupboard": Required[BoolValue],
        "ShipUnlockStored_File Cabinet": Required[BoolValue],
        "ShipUnlockStored_Inverse Teleporter": Required[BoolValue],
        "ShipUnlockStored_JackOLantern": Required[BoolValue],
        "ShipUnlockStored_Loud horn": Required[BoolValue],
        "ShipUnlockStored_Record player": Required[BoolValue],
        "ShipUnlockStored_Romantic table": Required[BoolValue],
        "ShipUnlockStored_Shower": Required[BoolValue],
        "ShipUnlockStored_Signal transmitter": Required[BoolValue],
        "ShipUnlockStored_Table": Required[BoolValue],
        "ShipUnlockStored_Teleporter": Required[BoolValue],
        "ShipUnlockStored_Television": Required[BoolValue],
        "ShipUnlockStored_Toilet": Required[BoolValue],
        "Stats_DaysSpent": Required[IntValue],
        "Stats_Deaths": Required[IntValue],
        "Stats_StepsTaken": Required[IntValue],
        "Stats_ValueCollected": Required[IntValue],
        "StoryLogs": Required[ArrayIntValue],
        "UnlockedShipObjects": Required[ArrayIntValue],
        "shipGrabbableItemIDs": ArrayIntValue,
        "shipGrabbableItemPos": ArrayVectorValue,
        "shipItemSaveData": ArrayIntValue,
        "shipScrapValues": ArrayIntValue,
    },
)
