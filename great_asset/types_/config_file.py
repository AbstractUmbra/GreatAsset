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

from typing import TypedDict

from .shared import *

__all__ = ("ConfigFile",)


class ConfigFile(TypedDict):
    TimesLanded: IntValue
    PlayerXPNum: IntValue
    PlayerLevel: IntValue
    FinishedShockMinigame: IntValue
    HostSettings_Public: BoolValue
    HostSettings_Name: StringValue
    LastVerPlayed: IntValue
    SpiderSafeMode: BoolValue
    InvertYAxis: BoolValue
    ScreenMode: IntValue
    FPSCap: IntValue
    Bindings: StringValue
    CurrentMic: StringValue
    PushToTalk: BoolValue
    MicEnabled: BoolValue
    LookSens: IntValue
    MasterVolume: FloatValue
    Gamma: FloatValue
    StartInOnlineMode: BoolValue
    PlayerFinishedSetup: BoolValue
    SelectedFile: IntValue
    LC_MoveObjectsTip: BoolValue
    LC_StorageTip: BoolValue
    LC_EclipseTip: BoolValue
    PlayedDungeonEntrance0: BoolValue
    PlayedDungeonEntrance1: BoolValue
    HasUsedTerminal: BoolValue
    LCTip_SellScrap: BoolValue
    LCTip_SecureDoors: BoolValue
    LCTip_UseManual: BoolValue
    LC_IntroTip1: BoolValue
