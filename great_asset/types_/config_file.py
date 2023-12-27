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
