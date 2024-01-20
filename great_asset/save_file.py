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

import random
from pathlib import Path
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from .crypt import decrypt, encrypt
from .enums import BestiaryEntry, ExtraUnlock, Item, Moon, Scrap, ShipUnlock
from .item import GrabbableScrap
from .utils import MISSING, SaveValue, _to_json, resolve_save_path  # type: ignore[reportPrivateUsage] we allow this here.
from .vector import Vector

if TYPE_CHECKING:
    from os import PathLike
    from types import TracebackType

    from typing_extensions import Self

    from .types_.challenge_file import ChallengeFile as ChallengeFileType
    from .types_.config_file import ConfigFile as ConfigFileType
    from .types_.save_file import (
        SaveFile as SaveFileType,
    )
    from .types_.shared import *

SaveT = TypeVar("SaveT", "SaveFileType", "ConfigFileType", "ChallengeFileType")

TEMP_FILE = Path("./_previously_decrypted_file.json")
TIPS = [
    "LC_MoveObjectsTip",
    "LC_StorageTip",
    "LC_LightningTip",
    "LCTip_SecureDoors",
    "LC_EclipseTip",
    "LCTip_SellScrap",
    "LCTip_UseManual",
    "LC_IntroTip1",
]

__all__ = (
    "SaveFile",
    "ConfigFile",
    "ChallengeFile",
)


class _BaseSaveFile(Generic[SaveT]):
    _inner_data: SaveT
    _file_type: str
    _extra_data: dict[str, Any]
    _written: bool
    _skip_parsing: bool

    __slots__ = (
        "_inner_data",
        "_file_type",
        "_extra_data",
        "_written",
        "_skip_parsing",
        "_raw_data",
    )

    def __init__(self, data: bytes, /) -> None:
        self._skip_parsing = False
        self._written = False

        self._raw_data: bytes = data
        self._parse_file()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        if not self._written and not exc_type:
            self.write()

    @classmethod
    def from_path(cls, path: Path | PathLike[Any] | str) -> Self:
        if not isinstance(path, Path):
            path = Path(path)

        if not path.exists():
            raise FileNotFoundError("The passed file is not found.")

        with path.open("rb") as fp:
            return cls(fp.read())

    def _parse_file(self) -> None:
        if self._skip_parsing:
            return

        data = decrypt(data=self._raw_data)

        self._validate_contents(data)

        self._inner_data = data

    def _upsert_value(self, key_name: str, value: Any) -> None:
        if value is MISSING:
            return  # If the value is the sentinel type, do nothing and move onto the next

        if isinstance(value, int):
            _type = "int"
        elif isinstance(value, list):
            if value and isinstance(value[0], int):
                _type = "System.Int32[],mscorlib"
            elif value and isinstance(value[0], dict):
                _type = "UnityEngine.Vector3[],UnityEngine.CoreModule"
            else:
                raise ValueError("Unexpected or unknown array type passed for `value`")
        elif isinstance(value, bool):
            _type = "bool"
        else:
            raise ValueError("Unexpected type passed for `value`: %r (%s)", value, type(value))

        try:
            self._inner_data[key_name]["value"] = value
        except KeyError:
            self._inner_data[key_name] = {"__type": _type, "value": value}

    def _dump(self, path: Path, /) -> None:
        decrypted_result = _to_json(self._inner_data)

        encoded = decrypted_result.encode()

        with TEMP_FILE.open("wb") as fp:
            fp.write(encoded)

        encrypted_result = encrypt(data=encoded)

        with path.open("wb") as fp:
            fp.write(encrypted_result)

    def write(self, *, path: Path | None = None) -> None:
        for key, value in self._extra_data.items():
            self._upsert_value(key, value)

        if path:
            self._dump(path)

        self._written = True

    def _validate_contents(self, data: SaveT, /) -> None:
        raise NotImplementedError


class SaveFile(_BaseSaveFile["SaveFileType"]):
    """
    A Lethal Company save file.

    Parameters
    -----------
    data: :class:`bytes`
        The data read from the save file.
    """

    # late init variable types
    _extra_data: dict[str, Any]

    _credits: int
    _current_planet_id: int
    _deadline: float
    _deaths: int
    _elapsed_days: int
    _quotas_met: int
    _quota_threshold: int
    _seed: int
    _steps_taken: int

    __slots__ = (
        "_inner_data",
        "_extra_data",
        "_credits",
        "_current_planet_id",
        "_current_quota_progress",
        "_deadline",
        "_deaths",
        "_elapsed_days",
        "_quotas_met",
        "_quota_threshold",
        "_seed",
        "_steps_taken",
        # these values need a richer interface
        "_enemy_scans",
        "_ship_item_save_data",
        "_unlocked_ship_objects",
        "_scrap",
        "__ship_grabbable_items",
        "__ship_grabbable_item_positions",
        "__ship_scrap",
    )

    @classmethod
    def resolve_from_file(cls, save_file_number: SaveValue, /) -> SaveFile:
        """
        A class method to find, open and return a save file from the default save file location (Windows) with the given file number.

        Parameters
        -----------
        save_file_number: Literal[``1``, ``2``, ``3``]
            The numbered save to open.
        """
        path = resolve_save_path(save_file_number)

        return cls.from_path(path)

    def _validate_contents(self, data: SaveFileType, /) -> None:
        _required_keys = (
            "GroupCredits",
            "DeadlineTime",
            "Stats_StepsTaken",
            "Stats_DaysSpent",
            "ProfitQuota",
            "CurrentPlanetID",
        )
        if any(key not in data for key in _required_keys):
            raise ValueError("This doesn't appear to be a valid Lethal Company save file!")

    def _generate_seed(self, *, max: int = 99999999, min: int = 10000000) -> int:
        return random.randint(min, max)

    def _parse_file(self) -> None:
        super()._parse_file()

        self._credits = self._inner_data["GroupCredits"]["value"]
        self._current_planet_id = self._inner_data["CurrentPlanetID"]["value"]
        self._current_quota_progress = self._inner_data["QuotaFulfilled"]["value"]
        self._deadline = self._inner_data["DeadlineTime"]["value"]
        self._deaths = self._inner_data["Stats_Deaths"]["value"]
        self._elapsed_days = self._inner_data["Stats_DaysSpent"]["value"]
        self._quotas_met = self._inner_data["QuotasPassed"]["value"]
        self._quota_threshold = self._inner_data["ProfitQuota"]["value"]
        self._seed = self._inner_data["RandomSeed"]["value"]
        self._steps_taken = self._inner_data["Stats_StepsTaken"]["value"]

        # TODO: richer interface here.
        self._enemy_scans = self._inner_data.get("EnemyScans", {"__type": "System.Int32[],mscorlib", "value": []})
        self._ship_item_save_data = self._inner_data.get(
            "shipItemSaveData", {"__type": "System.Int32[],mscorlib", "value": []}
        )
        self._unlocked_ship_objects = self._inner_data.get(
            "UnlockedShipObjects", {"__type": "System.Int32[],mscorlib", "value": []}
        )

        self.__ship_grabbable_items = self._inner_data.get(
            "shipGrabbableItemIDs", {"__type": "System.Int32[],mscorlib", "value": []}
        )
        self.__ship_grabbable_item_positions = self._inner_data.get(
            "shipGrabbableItemPos", {"__type": "UnityEngine.Vector3[],UnityEngine.CoreModule", "value": []}
        )
        self.__ship_scrap = self._inner_data.get("shipScrapValues", {"__type": "System.Int32[],mscorlib", "value": []})
        self._parse_scrap_mapping()

        # this key is mostly laziness for now
        # we'll serialise anything in here into the final payload
        # for now this will just be how we add the UnlockedStored_X keys
        self._extra_data = {}

    def _parse_scrap_mapping(self) -> None:
        # shipGrabbableItems contains all touchable items on the ship, including tools which have no value
        # shipScrapValues are an array of values assigned to each piece of scrap
        # it works because GrabbableItems[1]: ScrapValues[1], each index aligns and that's how the values are assigned, like a zip
        # once the scrapvalues runs out of elements, the rest of the items are treated as no value, like tools
        self._scrap: list[GrabbableScrap] = []

        for item, value, pos in zip(
            self.__ship_grabbable_items["value"], self.__ship_scrap["value"], self.__ship_grabbable_item_positions["value"]
        ):
            self._scrap.append(GrabbableScrap(item, value, pos))

        self.__ship_grabbable_items["value"] = self.__ship_grabbable_items["value"][len(self._scrap) :]
        self.__ship_grabbable_item_positions["value"] = self.__ship_grabbable_item_positions["value"][len(self._scrap) :]

    @property
    def credits(self) -> int:
        """
        Get the current credits value within the save.

        Returns
        --------
        :class:`int`
        """
        return self._credits

    @property
    def current_moon(self) -> Moon:
        """
        Get the current planet within the save.

        Returns
        --------
        :class:`~great_asset.Moon`
        """
        return Moon(self._current_planet_id)

    @property
    def steps_taken(self) -> int:
        """
        Get the current amount of steps taken within the save file.

        Returns
        --------
        :class:`int`
        """
        return self._steps_taken

    @property
    def deaths(self) -> int:
        """
        Get the current amount of deaths within the save file.

        Returns
        --------
        :class:`int`
        """
        return self._deaths

    @property
    def elapsed_days(self) -> int:
        """
        Get the current amount of elapsed days within the save file.

        Returns
        --------
        :class:`int`
        """
        return self._elapsed_days

    @property
    def deadline(self) -> int:
        """
        Get the current deadline in time as days within the save file.


        .. warning:
            I round this value using :meth:`round` so it may not be fully accurate.
            If you need the raw value, try :property:`raw_deadline`.

        Returns
        --------
        :class:`int`
        """
        return round(self._deadline / 1080)

    @property
    def raw_deadline(self) -> float:
        """
        Get the current deadline in time's raw value within the save file.

        Returns
        --------
        :class:`float`
        """
        return self._deadline

    @property
    def profit_quota(self) -> int:
        """
        Get the current profit quota (value to reach) within the save file.

        Returns
        --------
        :class:`int`
        """
        return self._quota_threshold

    @property
    def quotas_passed(self) -> int:
        """
        Get the current total quotas met from within the save file.

        Returns
        --------
        :class:`int`
        """
        return self._quotas_met

    @property
    def current_quota_progress(self) -> int:
        """
        Get the current quota progress from within the save file.

        Returns
        --------
        :class:`int`
        """
        return self._current_quota_progress

    @property
    def current_seed(self) -> int:
        """
        Get the current seed from within the save file.

        Returns
        --------
        :class:`int`
        """
        return self._seed

    def update_credits(self, new_credits: int, /) -> None:
        """Update the credits value within the save file.

        Parameters
        -----------
        new_credits: :class:`int`
            The new credits value.
        """
        self._upsert_value("GroupCredits", new_credits)
        self._credits = new_credits

    def update_current_moon(self, moon: Moon, /) -> None:
        """
        Update the current planet within the save file.

        Parameters
        -----------
        planet: :class:`~great_asset.Moon`
            The planet to update to.
        """
        self._upsert_value("CurrentPlanetID", moon.value)
        self._current_planet_id = moon.value

    def update_steps_taken(self, new_steps: int, /) -> None:
        """
        Update the current amount of steps taken within the save file.

        Parameters
        -----------
        new_steps: :class:`int`
            The amount of steps to have taken.
        """
        self._upsert_value("Stats_StepsTaken", new_steps)
        self._steps_taken = new_steps

    def update_deaths(self, new_deaths: int, /) -> None:
        """
        Update the current deaths within the save file.

        Parameters
        -----------
        new_deaths: :class:`int`
            The new value for total deaths.
        """
        self._upsert_value("Stats_Deaths", new_deaths)
        self._deaths = new_deaths

    def update_elapsed_days(self, new_elapsed_days: int, /) -> None:
        """
        Update the elapsed days count within the save file.

        Parameters
        -----------
        new_elapsed_days: :class:`int`
            The elapsed days value.
        """
        self._upsert_value("Stats_DaysSpent", new_elapsed_days)
        self._elapsed_days = new_elapsed_days

    def update_deadline(self, new_deadline: int | float, /) -> None:
        """
        Update the deadline time within the save file.

        Parameters
        -----------
        new_deadline: :class:`int` | :class:`float`
            New deadline/time remaining in days or minutes.
        """
        if not isinstance(new_deadline, float):
            new_deadline = new_deadline * 1080

        self._upsert_value("DeadlineTime", new_deadline)
        self._deadline = new_deadline

    def update_profit_quota(self, new_profit_quota: int, /) -> None:
        """
        Update the target quota value within the save file.

        Parameters
        -----------
        new_profit_quota: :class:`int`
            The profit quota to set.
        """
        self._upsert_value("ProfitQuota", new_profit_quota)
        self._quota_threshold = new_profit_quota

    def update_quotas_met(self, new_quotas_met: int, /) -> None:
        """
        Updates the quotas met within the save file.

        Parameters
        -----------
        new_quotas_met: :class:`int`
            The quotas met to set.
        """
        self._upsert_value("QuotasPassed", new_quotas_met)
        self._quotas_met = new_quotas_met

    def update_current_quota_progress(self, new_quota_progress: int, /) -> None:
        """
        Updates the current quota progress within the save file.

        Parameters
        -----------
        new_quota_progress: :class:`int`
            The quota progress to set.
        """
        self._upsert_value("QuotaFulfilled", new_quota_progress)
        self._current_quota_progress = new_quota_progress

    def update_current_seed(self, new_seed: int | None = None, /) -> None:
        """
        Updates the current seed within the save file.

        Parameters
        -----------
        new_seed: :class:`int` | :class:`None`
            The new seed to update to. If ``None`` is passed or no value is given a random one will be generated.
        """
        seed = new_seed or self._generate_seed()

        self._upsert_value("RandomSeed", seed)
        self._seed = seed

    def unlock_ship_upgrades(self, *items: ShipUnlock) -> None:
        """
        Unlock upgrades for the ship.

        Parameters
        -----------
        *items: :class:`~great_asset.ShipUnlock`
            The items to unlock in the ship.


        .. note::
            The items unlocked will be added into storage, please access them from the terminal to place them.
        """
        for item in items:
            self._unlocked_ship_objects["value"].append(item.serialised_value)
            self._extra_data[f"ShipUnlockStored_{item.serialised_name}"] = True

    def unlock_all_ship_upgrades(self) -> None:
        """
        Unlocks all possible ship upgrades.
        """
        return self.unlock_ship_upgrades(*ShipUnlock.all())

    def remove_ship_upgrades(self, *items: ShipUnlock) -> None:
        """
        Remove upgrades from the ship.

        Parameters
        -----------
        *items: :class:`~great_asset.ShipUnlock`
            The items to remove from the ship.
        """
        for item in items:
            try:
                self._unlocked_ship_objects["value"].remove(item.serialised_value)
            except ValueError:
                pass
            self._extra_data[f"ShipUnlockStored_{item.serialised_name}"] = False

    def unlock_extras(self, *items: ExtraUnlock) -> None:
        """
        Unlock other items within the ship or for the player(s).

        Parameters
        -----------
        *items: :class:`~great_asset.ExtraUnlock`
            The items to unlock.
        """
        self._unlocked_ship_objects["value"] = list({i.value for i in items})

    def unlock_all_ship_extras(self) -> None:
        """
        Unlock all possible ship extras.
        """
        return self.unlock_extras(*ExtraUnlock.all())

    def unlock_bestiary_entries(self, *entries: BestiaryEntry) -> None:
        """
        Unlock bestiary entries on the ship terminal.

        Parameters
        -----------
        *entries: :class:`~great_asset.BestiaryEntry`
            The entries to unlock.
        """
        self._enemy_scans["value"] = list({e.value for e in entries})

    def unlock_all_bestiary_entries(self) -> None:
        """
        Unlock all possible bestiary entries.
        """
        return self.unlock_bestiary_entries(*BestiaryEntry.all())

    def spawn_items(self, *items: tuple[Item | Scrap, Vector | None], value_min: int = 30, value_max: int = 90) -> None:
        """
        Spawn items within the world or ship.

        Parameters
        -----------
        *items: tuple[:class:`~great_asset.Item` | :class:`~great_asset.Scrap`, :class:`~great_asset.Vector` | :class:`None`]
            A series of tuples with the item and it's position to spawn in.
            Using ``None`` as the second value will spawn at a default area near the door of the ship internally.
        """
        cupboard_position = self._inner_data.get("ShipUnlockPos_Cupboard")

        for item, position in items:
            vec = position or Vector.in_cupboard(cupboard_position=cupboard_position)
            if isinstance(item, Scrap):
                value = random.randint(value_min, value_max)
                self._scrap.append(GrabbableScrap(item.value, value, vec.serialise()))
                continue

            self.__ship_grabbable_items["value"].append(item.value)
            self.__ship_grabbable_item_positions["value"].append(vec.serialise())

    def get_current_items(self) -> list[Item]:
        """
        Get the current items that exist within the ship in the save file.

        Returns
        --------
        list[:class:`~great_asset.Item`]
        """
        return [Item(item) for item in self.__ship_grabbable_items["value"]]

    def get_current_scrap(self) -> list[Scrap]:
        """
        Get the current scrap that exist within the ship in the save file.

        Returns
        --------
        list[:class:`~great_asset.Scrap`]
        """
        return [Scrap(item.id) for item in self._scrap]

    def write(self, *, path: Path | None = None) -> None:
        """
        A function to write the save file data to the internal data structure.

        Parameters
        -----------
        dump_to_file: :class:`bool`
            Whether to overwrite the passed file with the changes. Defaults to ``True``.
        overwrite: :class:`bool`
            Whether to overwrite the existing save file with the changes. Defaults to ``True``.
            Irrelevant if ``dump_to_file`` is ``False``.
            Creates a file with the same name with the file extension of ``".over"``.
        """
        # manually handle the more complex types:
        self._upsert_value("UnlockedShipObjects", list(set(self._unlocked_ship_objects["value"])))
        self._inner_data["EnemyScans"] = self._enemy_scans
        self._inner_data["shipItemSaveData"] = self._ship_item_save_data

        for item in self._scrap:
            self.__ship_scrap["value"].insert(0, item.value)
            self.__ship_grabbable_items["value"].insert(0, item.id)
            self.__ship_grabbable_item_positions["value"].insert(0, item.pos)

        self._inner_data["shipScrapValues"] = self.__ship_scrap
        self._inner_data["shipGrabbableItemIDs"] = self.__ship_grabbable_items
        self._inner_data["shipGrabbableItemPos"] = self.__ship_grabbable_item_positions

        super().write(path=path)


class ConfigFile(_BaseSaveFile["ConfigFileType"]):
    _extra_data: dict[str, Any]

    # late init types
    arachnophobia_mode: bool
    y_axis_inverted: bool
    screen_mode: int
    fps_mode: int
    current_mic: str
    push_to_talk: bool
    mic_enabled: bool
    mouse_sensitivity: int
    master_volume: float
    gamma: float
    finished_setup: bool
    start_online: bool

    _player_xp: IntValue
    _player_level: IntValue
    _times_landed: IntValue
    _is_host_public: BoolValue
    _host_name: StringValue
    _played_extrance_0: BoolValue
    _played_entrance_1: BoolValue
    _tips: dict[str, BoolValue]

    def _validate_contents(self, data: ConfigFileType, /) -> None:
        _required_keys = ("SelectedFile", "FPSCap", "Gamma", "LookSens", "ScreenMode")
        if any(key not in data for key in _required_keys):
            raise ValueError("This doesn't appear to be a valid Lethal Company config file!")

    def _parse_file(self) -> None:
        super()._parse_file()

        self.arachnophobia_mode = self._inner_data["SpiderSafeMode"]["value"]
        self.y_axis_inverted = self._inner_data["InvertYAxis"]["value"]
        self.screen_mode = self._inner_data["ScreenMode"]["value"]
        self.fps_mode = self._inner_data["FPSCap"]["value"]
        self.current_mic = self._inner_data["CurrentMic"]["value"]
        self.push_to_talk = self._inner_data["PushToTalk"]["value"]
        self.mic_enabled = self._inner_data["MicEnabled"]["value"]
        self.mouse_sensitivity = self._inner_data["LookSens"]["value"]
        self.master_volume = self._inner_data["MasterVolume"]["value"]
        self.gamma = self._inner_data["Gamma"]["value"]
        self.finished_setup = self._inner_data["PlayerFinishedSetup"]["value"]
        self.start_online = self._inner_data["StartInOnlineMode"]["value"]

        self._player_xp = self._inner_data.get("PlayerXPNum", MISSING)
        self._player_level = self._inner_data.get("PlayerLevel", MISSING)
        self._times_landed = self._inner_data.get("TimesLanded", MISSING)
        self._is_host_public = self._inner_data.get("HostSettings_Public", MISSING)
        self._host_name = self._inner_data.get("HostSettings_Name", MISSING)
        self._played_entrance_0 = self._inner_data.get("PlayedDungeonEntrance0", MISSING)
        self._played_entrance_1 = self._inner_data.get("PlayedDungeonEntrance1", MISSING)
        self._tips = {tip: self._inner_data.get(tip, MISSING) for tip in TIPS}
        self._extra_data = {}

    @property
    def player_xp(self) -> int:
        if self._player_xp is not MISSING:
            return self._player_xp["value"]
        return 0

    @property
    def player_level(self) -> int:
        if self._player_xp is not MISSING:
            return self._player_level["value"]
        return 0

    @property
    def times_landed(self) -> int:
        if self._times_landed is not MISSING:
            return self._times_landed["value"]
        return 0

    @property
    def is_host_public(self) -> bool:
        if self._is_host_public is not MISSING:
            return self._is_host_public["value"]
        return False

    @property
    def host_name(self) -> str:
        if self._host_name is not MISSING:
            return self._host_name["value"]
        return "No name set"

    @property
    def played_entrances(self) -> list[int]:
        return [val["value"] for val in [self._played_entrance_0, self._played_entrance_1] if val is not MISSING]

    @property
    def tips(self) -> dict[str, bool]:
        return {tip: value["value"] for tip, value in self._tips.items() if value is not MISSING}

    def set_player_xp(self, value: int) -> None:
        if 0 <= value <= 999:
            self._player_xp = {"__type": "int", "value": value}

    def set_player_level(self, value: int) -> None:
        if value > 0:
            self._player_level = {"__type": "int", "value": (value - 1) % 5}

    def set_host_public(self, value: bool) -> None:
        self._is_host_public = {"__type": "bool", "value": value}

    def set_host_name(self, value: str) -> None:
        self._host_name = {"__type": "string", "value": value[40:]}

    def set_arachnophobia_mode(self, value: bool) -> None:
        self.arachnophobia_mode = value

    def set_inverted_y_axis(self, value: bool) -> None:
        self.y_axis_inverted = value

    def set_screen_mode(self, value: int) -> None:
        self.screen_mode = value

    def set_fps_mode(self, value: int) -> None:
        self.fps_mode = value

    def set_push_to_talk(self, value: bool) -> None:
        self.push_to_talk = value

    def set_mic_enabled(self, value: bool) -> None:
        self.mic_enabled = value

    def set_mouse_sensitivity(self, value: int) -> None:
        self.mouse_sensitivity = value

    def set_master_volume(self, value: float) -> None:
        if 0 <= value <= 1:
            self.master_volume = value

    def set_gamma(self, value: float) -> None:
        if 0 <= value <= 1:
            self.gamma = value

    def write(self, *, path: Path | None = None) -> None:
        self._upsert_value("SpiderSafeMode", self.arachnophobia_mode)
        self._upsert_value("InvertYAxis", self.y_axis_inverted)
        self._upsert_value("ScreenMode", self.screen_mode)
        self._upsert_value("FPSCap", self.fps_mode)
        self._upsert_value("CurrentMic", self.current_mic)
        self._upsert_value("PushToTalk", self.push_to_talk)
        self._upsert_value("MicEnabled", self.mic_enabled)
        self._upsert_value("LookSens", self.mouse_sensitivity)
        self._upsert_value("MasterVolume", self.master_volume)
        self._upsert_value("Gamma", self.gamma)
        self._upsert_value("PlayerFinishedSetup", self.finished_setup)
        self._upsert_value("StartInOnlineMode", self.start_online)
        self._upsert_value("PlayerXPNum", self._player_xp)
        self._upsert_value("PlayerLevel", self._player_level)
        self._upsert_value("TimesLanded", self._times_landed)
        self._upsert_value("HostSettings_Public", self._is_host_public)
        self._upsert_value("HostSettings_Name", self._host_name)
        self._upsert_value("PlayedDungeonEntrance0", self._played_entrance_0)
        self._upsert_value("PlayedDungeonEntrance1", self._played_entrance_1)

        for idx, tip in enumerate(self._tips):
            self._upsert_value(TIPS[idx], tip)

        super().write(path=path)


class ChallengeFile(_BaseSaveFile["ChallengeFileType"]):
    _profit_earned: int
    _finished_challenge: bool
    _submitted_score: bool
    _file_game_version: int
    _challenge_week_number: int
    _set_challenge_file_money: bool

    __slots__ = (
        "_profit_earned",
        "_finished_challenge",
        "_submitted_score",
        "_file_game_version",
        "_challenge_week_number",
        "_set_challenge_file_money",
    )

    def _validate_contents(self, data: ChallengeFileType) -> None:
        _required_keys = ("ProfitEarned", "FinishedChallenge", "SubmittedScore")
        if any(key not in data for key in _required_keys):
            raise ValueError("This doesn't appear to be a valid Challenge file.")

    def _parse_file(self) -> None:
        super()._parse_file()

        self._profit_earned = self._inner_data["ProfitEarned"]["value"]
        self._finished_challenge = self._inner_data["FinishedChallenge"]["value"]
        self._submitted_score = self._inner_data["SubmittedScore"]["value"]
        self._file_game_version = self._inner_data.get("FileGameVers", {"__type": "int", "value": 48})["value"]
        self._challenge_week_number = self._inner_data.get("FileGameVers", {"__type": "int", "value": 4})["value"]
        self._set_challenge_file_money = self._inner_data.get("SetChallengeFileMoney", {"__type": "bool", "value": False})[
            "value"
        ]

        self._extra_data = {}

    @property
    def profit_earned(self) -> int:
        return self._profit_earned

    @property
    def finished_challenge(self) -> bool:
        return self._finished_challenge

    @property
    def submitted_score(self) -> int:
        return self._submitted_score

    @property
    def file_game_version(self) -> int:
        return self._file_game_version

    @property
    def challenge_week_number(self) -> int:
        return self._challenge_week_number

    @property
    def set_challenge_file_money(self) -> bool:
        return self._set_challenge_file_money
