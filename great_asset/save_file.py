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

from pathlib import Path
from typing import TYPE_CHECKING, Any

from .crypt import decrypt, encrypt
from .utils import _to_json  # type: ignore # we'll allow this private usage for now

if TYPE_CHECKING:
    from os import PathLike

    from .enums import ShipUnlocks
    from .types_.save_file import (
        InnerVectorValue,
        SaveFile as SaveFileType,
    )

TEMP_FILE = Path("./_previously_decrypted_file.json")


class SaveFile:
    # late init variable types
    _inner_data: SaveFileType
    current_planet_id: int
    credits: int
    deadline: int
    steps: int
    elapsed_days: int
    deaths: int
    quota_threshold: int
    quotas_met: int
    seed: int

    _passed_current_quota: int
    _extra_data: dict[str, Any]

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

        self.current_planet_id = data["CurrentPlanetID"]["value"]
        self.credits = data["GroupCredits"]["value"]
        self.deadline = data["DeadlineTime"]["value"]
        self.steps = data["Stats_StepsTaken"]["value"]
        self.elapsed_days = data["Stats_DaysSpent"]["value"]
        self.deaths = data["Stats_Deaths"]["value"]
        self.quota_threshold = data["ProfitQuota"]["value"]
        self.quotas_met = data["QuotasPassed"]["value"]
        self.seed = data["RandomSeed"]["value"]

        self._enemy_scans = data.get("EnemyScans", {"__type": "System.Int32[],mscorlib", "value": []})
        self._passed_current_quota = data["QuotaFulfilled"]["value"]
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
    def current_quota_met(self) -> bool:
        return bool(self._passed_current_quota)

    @property
    def enemy_scans(self) -> list[int]:
        return self._enemy_scans.get("value", [])

    @property
    def ship_item_save_data(self) -> list[int]:
        return self._ship_item_save_data.get("value", [])

    @property
    def ship_scrap(self) -> list[int]:
        return self._ship_scrap.get("value", [])

    @property
    def ship_grabbable_items(self) -> list[int]:
        return self._ship_grabbable_items.get("value", [])

    @property
    def ship_grabbable_item_positions(self) -> list[InnerVectorValue]:
        return self._ship_grabbable_item_positions.get("value", [])

    @property
    def unlocked_ship_objects(self) -> list[int]:
        return self._unlocked_ship_objects.get("value", [])

    def unlock_ship_upgrades(self, *items: ShipUnlocks) -> None:
        for item in items:
            self.unlocked_ship_objects.append(item.serialised_value)
            self._extra_data[f"ShipUnlockStored_{item.serialised_name}"] = True

    def remove_ship_upgrades(self, *items: ShipUnlocks) -> None:
        for item in items:
            try:
                self.unlocked_ship_objects.remove(item.serialised_value)
            except ValueError:
                pass
            self._extra_data[f"ShipUnlockStored_{item.serialised_name}"] = False

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

    def serialise(self, *, write: bool = True) -> None:
        self._upsert_value("GroupCredits", self.credits)
        self._upsert_value("DeadlineTime", self.deadline)
        self._upsert_value("Stats_StepsTaken", self.steps)
        self._upsert_value("Stats_Deaths", self.deaths)
        self._upsert_value("Stats_DaysSpent", self.elapsed_days)

        self._upsert_value("ProfitQuota", self.quota_threshold)
        self._upsert_value("QuotasPassed", self.quotas_met)
        self._upsert_value("QuotaFulfilled", self._passed_current_quota)
        self._upsert_value("RandomSeed", self.seed)
        self._upsert_value("CurrentPlanetID", self.current_planet_id)

        self._upsert_value("UnlockedShipObjects", list(set(self.unlocked_ship_objects)))

        # manually handle the more complex types:
        self._inner_data["shipScrapValues"] = self._ship_scrap
        self._inner_data["shipGrabbableItemIDs"] = self._ship_grabbable_items
        self._inner_data["shipGrabbableItemPos"] = self._ship_grabbable_item_positions
        self._inner_data["shipItemSaveData"] = self._ship_item_save_data

        for key, value in self._extra_data.items():
            self._upsert_value(key, value)

        if write:
            self.dump()

    def dump(self) -> None:
        decrypted_result = _to_json(self._inner_data)

        with TEMP_FILE.open("wb") as fp:
            fp.write(decrypted_result.encode("utf-8"))

        encrypted_result = encrypt(TEMP_FILE)

        with self.path.open("wb") as fp:
            fp.write(encrypted_result)
