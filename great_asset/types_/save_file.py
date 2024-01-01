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

from typing import Required, TypedDict

from .shared import *

__all__ = ("SaveFile",)


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
        "ShipUnlockStored_Bunkbeds": Required[BoolValue],
        "ShipUnlockMoved_Bunkbeds": BoolValue,
        "ShipUnlockPos_Bunkbeds": VectorValue,
        "ShipUnlockRot_Bunkbeds": VectorValue,
        "ShipUnlockStored_Cupboard": Required[BoolValue],
        "ShipUnlockMoved_Cupboard": BoolValue,
        "ShipUnlockPos_Cupboard": VectorValue,
        "ShipUnlockRot_Cupboard": VectorValue,
        "ShipUnlockStored_File Cabinet": Required[BoolValue],
        "ShipUnlockMoved_File Cabinet": BoolValue,
        "ShipUnlockPos_File Cabinet": VectorValue,
        "ShipUnlockRot_File Cabinet": VectorValue,
        "ShipUnlockStored_Light switch": Required[BoolValue],
        "ShipUnlockMoved_Light switch": BoolValue,
        "ShipUnlockPos_Light switch": VectorValue,
        "ShipUnlockRot_Light switch": VectorValue,
        "ShipUnlockStored_Loud horn": Required[BoolValue],
        "ShipUnlockMoved_Loud horn": BoolValue,
        "ShipUnlockPos_Loud horn": VectorValue,
        "ShipUnlockRot_Loud horn": VectorValue,
        "ShipUnlockStored_Teleporter": Required[BoolValue],
        "ShipUnlockMoved_Teleporter": BoolValue,
        "ShipUnlockPos_Teleporter": VectorValue,
        "ShipUnlockRot_Teleporter": VectorValue,
        "ShipUnlockStored_Terminal": Required[BoolValue],
        "ShipUnlockMoved_Terminal": BoolValue,
        "ShipUnlockPos_Terminal": VectorValue,
        "ShipUnlockRot_Terminal": VectorValue,
        "ShipUnlockStored_Inverse Teleporter": Required[BoolValue],
        "ShipUnlockMoved_Inverse Teleporter": BoolValue,
        "ShipUnlockPos_Inverse Teleporter": VectorValue,
        "ShipUnlockRot_Inverse Teleporter": VectorValue,
        "ShipUnlockStored_JackOLantern": Required[BoolValue],
        "ShipUnlockMoved_JackOLantern": BoolValue,
        "ShipUnlockPos_JackOLantern": VectorValue,
        "ShipUnlockRot_JackOLantern": VectorValue,
        "ShipUnlockStored_Record player": Required[BoolValue],
        "ShipUnlockMoved_Record player": BoolValue,
        "ShipUnlockPos_Record player": VectorValue,
        "ShipUnlockRot_Record player": VectorValue,
        "ShipUnlockStored_Romantic table": Required[BoolValue],
        "ShipUnlockMoved_Romantic table": BoolValue,
        "ShipUnlockPos_Romantic table": VectorValue,
        "ShipUnlockRot_Romantic table": VectorValue,
        "ShipUnlockStored_Shower": Required[BoolValue],
        "ShipUnlockMoved_Shower": BoolValue,
        "ShipUnlockPos_Shower": VectorValue,
        "ShipUnlockRot_Shower": VectorValue,
        "ShipUnlockStored_Signal translator": Required[BoolValue],
        "ShipUnlockMoved_Signal translator": BoolValue,
        "ShipUnlockPos_Signal translator": VectorValue,
        "ShipUnlockRot_Signal translator": VectorValue,
        "ShipUnlockStored_Table": Required[BoolValue],
        "ShipUnlockMoved_Table": BoolValue,
        "ShipUnlockPos_Table": VectorValue,
        "ShipUnlockRot_Table": VectorValue,
        "ShipUnlockStored_Television": Required[BoolValue],
        "ShipUnlockMoved_Television": BoolValue,
        "ShipUnlockPos_Television": VectorValue,
        "ShipUnlockRot_Television": VectorValue,
        "ShipUnlockStored_Toilet": Required[BoolValue],
        "ShipUnlockMoved_Toilet": BoolValue,
        "ShipUnlockPos_Toilet": VectorValue,
        "ShipUnlockRot_Toilet": VectorValue,
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
