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
from typing import TYPE_CHECKING, Any

from .crypt import decrypt, encrypt
from .enums import Moon
from .utils import _to_json  # type: ignore # we'll allow this private usage for now

if TYPE_CHECKING:
    from os import PathLike

    from .enums import ExtraUnlock, ShipUnlock
    from .types_.save_file import (
        SaveFile as SaveFileType,
    )

TEMP_FILE = Path("./_previously_decrypted_file.json")


class SaveFile:
    # late init variable types
    _inner_data: SaveFileType
    _extra_data: dict[str, Any]

    _credits: int
    _current_planet_id: int
    _deadline: int
    _deaths: int
    _elapsed_days: int
    _quotas_met: int
    _quota_threshold: int
    _seed: int
    _steps_taken: int

    __slots__ = (
        "_inner_data",
        "_extra_data",  # hopefully not for long
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
        "_ship_scrap",
        "_ship_grabbable_items",
        "_ship_grabbable_item_positions",
        "_ship_item_save_data",
        "_unlocked_ship_objects",
        "path",
    )

    def __init__(self, path: str | PathLike[str] | Path, /) -> None:
        if not isinstance(path, Path):
            path = Path(path)

        if not path.exists():
            raise ValueError("The path given does not exist")

        self.path: Path = path
        self._parse_file()

    def _parse_file(self) -> None:
        data = decrypt(self.path)

        if not any(
            [
                data.get("GroupCredits"),
                data.get("DeadlineTime"),
                data.get("Stats_StepsTaken"),
                data.get("Stats_DaysSpent"),
                data.get("ProfitQuota"),
                data.get("CurrentPlanetID"),
            ]
        ):
            raise ValueError("This doesn't appear to be a valid Lethal Company save file!")

        self._inner_data = data

        self._credits = data["GroupCredits"]["value"]
        self._current_planet_id = data["CurrentPlanetID"]["value"]
        self._current_quota_progress = data["QuotaFulfilled"]["value"]
        self._deadline = data["DeadlineTime"]["value"]
        self._deaths = data["Stats_Deaths"]["value"]
        self._elapsed_days = data["Stats_DaysSpent"]["value"]
        self._quotas_met = data["QuotasPassed"]["value"]
        self._quota_threshold = data["ProfitQuota"]["value"]
        self._seed = data["RandomSeed"]["value"]
        self._steps_taken = data["Stats_StepsTaken"]["value"]

        # TODO: richer interface here.
        self._enemy_scans = data.get("EnemyScans", {"__type": "System.Int32[],mscorlib", "value": []})
        self._ship_scrap = data.get("shipScrapValues", {"__type": "System.Int32[],mscorlib", "value": []})
        self._ship_grabbable_items = data.get("shipGrabbableItemIDs", {"__type": "System.Int32[],mscorlib", "value": []})
        self._ship_grabbable_item_positions = data.get(
            "shipGrabbableItemPos", {"__type": "UnityEngine.Vector3[],UnityEngine.CoreModule", "value": []}
        )
        self._ship_item_save_data = data.get("shipItemSaveData", {"__type": "System.Int32[],mscorlib", "value": []})
        self._unlocked_ship_objects = data.get("UnlockedShipObjects", {"__type": "System.Int32[],mscorlib", "value": []})

        # this key is mostly laziness for now
        # we'll serialise anything in here into the final payload
        # for now this will just be how we add the UnlockedStored_X keys
        self._extra_data = {}

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
        Get the current deadline in time within the save file.

        Returns
        --------
        :class:`int`
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

    def update_current_moon(self, moon: Moon, /) -> None:
        """
        Update the current planet within the save file.

        Parameters
        -----------
        planet: :class:`~great_asset.Moon`
            The planet to update to.
        """
        self._upsert_value("CurrentPlanetID", moon.value)

    def update_steps_taken(self, new_steps: int, /) -> None:
        """
        Update the current amount of steps taken within the save file.

        Parameters
        -----------
        new_steps: :class:`int`
            The amount of steps to have taken.
        """
        self._upsert_value("Stats_StepsTaken", new_steps)

    def update_deaths(self, new_deaths: int, /) -> None:
        """
        Update the current deaths within the save file.

        Parameters
        -----------
        new_deaths: :class:`int`
            The new value for total deaths.
        """
        self._upsert_value("Stats_Deaths", new_deaths)

    def update_elapsed_dats(self, new_elapsed_days: int, /) -> None:
        """
        Update the elapsed days count within the save file.

        Parameters
        -----------
        new_elapsed_days: :class:`int`
            The elapsed days value.
        """
        self._upsert_value("Stats_DaysSpent", new_elapsed_days)

    def update_deadline(self, new_deadline: int, /) -> None:
        """
        Update the deadline time within the save file.

        Parameters
        -----------
        new_deadline: :class:`int`
            New deadline/time remaining in days*24*60 minutes.
        """
        self._upsert_value("DeadlineTime", new_deadline)

    def update_profit_quota(self, new_profit_quota: int, /) -> None:
        """
        Update the target quota value within the save file.

        Parameters
        -----------
        new_profit_quota: :class:`int`
            The profit quota to set.
        """
        self._upsert_value("ProfitQuota", new_profit_quota)

    def update_quotas_met(self, new_quotas_met: int, /) -> None:
        """
        Updates the quotas met within the save file.

        Parameters
        -----------
        new_quotas_met: :class:`int`
            The quotas met to set.
        """
        self._upsert_value("QuotasPassed", new_quotas_met)

    def update_current_quota_progress(self, new_quota_progress: int, /) -> None:
        """
        Updates the current quota progress within the save file.

        Parameters
        -----------
        new_quota_progress: :class:`int`
            The quota progress to set.
        """
        self._upsert_value("QuotaFulfilled", new_quota_progress)

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
        for item in items:
            self._unlocked_ship_objects["value"].append(item.value)

    def _generate_seed(self, *, max: int = 99999999, min: int = 10000000) -> int:
        return random.randint(min, max)

    def _upsert_value(self, key_name: str, value: Any) -> None:
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

    def write(self, *, dump_to_file: bool = True) -> None:
        """
        A function to write the save file data to the internal data structure.

        Parameters
        -----------
        dump_to_file: :class:`bool`
            Whether to overwrite the passed file with the changes. Defaults to ``True``.
        """
        # manually handle the more complex types:
        self._upsert_value("UnlockedShipObjects", list(set(self._unlocked_ship_objects["value"])))
        self._inner_data["shipScrapValues"] = self._ship_scrap
        self._inner_data["shipGrabbableItemIDs"] = self._ship_grabbable_items
        self._inner_data["shipGrabbableItemPos"] = self._ship_grabbable_item_positions
        self._inner_data["shipItemSaveData"] = self._ship_item_save_data

        for key, value in self._extra_data.items():
            self._upsert_value(key, value)

        if dump_to_file:
            self._dump()

    def _dump(self) -> None:
        decrypted_result = _to_json(self._inner_data)

        with TEMP_FILE.open("wb") as fp:
            fp.write(decrypted_result.encode("utf-8"))

        encrypted_result = encrypt(TEMP_FILE)

        with self.path.open("wb") as fp:
            fp.write(encrypted_result)
