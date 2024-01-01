# pyright: reportPrivateUsage=false
# this is okay in tests


from __future__ import annotations

from pathlib import Path
from typing import Literal

import pytest

from great_asset import Moon, SaveFile, ShipUnlock

BASE_PATH = Path(__file__).parent


def make_save(number: Literal[1, 2, 3]) -> SaveFile:
    path = BASE_PATH / f"./save_files/LCSaveFile{number}"
    return SaveFile(path)


class TestSaveFile:
    def test_credit_changes(self) -> None:
        # check default values

        save_file_1 = make_save(1)
        save_file_2 = make_save(2)
        assert save_file_1.credits == 1605
        assert save_file_2.credits == 585

        save_file_1.update_credits(2820)
        save_file_2.update_credits(312)

        save_file_1.write(dump_to_file=False)
        assert save_file_1._inner_data["GroupCredits"]["value"] == 2820

        save_file_2.write(dump_to_file=False)
        assert save_file_2._inner_data["GroupCredits"]["value"] == 312

    def test_adding_teleporter(self) -> None:
        save_file_1 = make_save(1)

        save_file_1.unlock_ship_upgrades(ShipUnlock.teleporter)

        save_file_1.write(dump_to_file=False)

        assert (
            ShipUnlock.teleporter.serialised_value in save_file_1._inner_data["UnlockedShipObjects"]["value"]
            and save_file_1._inner_data["ShipUnlockStored_Teleporter"]["value"] is True
        )

    def test_removing_teleporter(self) -> None:
        save_file_2 = make_save(2)

        save_file_2.unlock_ship_upgrades(ShipUnlock.teleporter)

        save_file_2.remove_ship_upgrades(ShipUnlock.teleporter)

        save_file_2.write(dump_to_file=False)

        assert (
            ShipUnlock.teleporter.serialised_value not in save_file_2._inner_data["UnlockedShipObjects"]["value"]
            and save_file_2._inner_data["ShipUnlockStored_Teleporter"]["value"] is False
        )

    @pytest.mark.parametrize("moon", [(Moon.titan), (Moon.assurance), (Moon.offense)])
    def test_editing_moon(self, moon: Moon) -> None:
        save = make_save(1)

        assert save.current_moon is Moon.company_building

        save.update_current_moon(moon)

        assert save.current_moon is moon
        assert save._inner_data["CurrentPlanetID"]["value"] == moon.value

    @pytest.mark.parametrize("steps", [(69), (420), (69420)])
    def test_editing_steps_taken(self, steps: int) -> None:
        save = make_save(2)

        assert save.steps_taken == 39344

        save.update_steps_taken(steps)

        assert save.steps_taken == steps
        assert save._inner_data["Stats_StepsTaken"]["value"] == steps

    @pytest.mark.parametrize("deaths", [(69), (420), (69420)])
    def test_editing_deaths(self, deaths: int) -> None:
        save = make_save(1)

        assert save.deaths == 10

        save.update_deaths(deaths)

        assert save.deaths == deaths
        assert save._inner_data["Stats_Deaths"]["value"] == deaths

    @pytest.mark.parametrize("days", [(69), (420), (69420)])
    def test_editing_elapsed_days(self, days: int) -> None:
        save = make_save(2)

        assert save.elapsed_days == 5

        save.update_elapsed_days(days)

        assert save.elapsed_days == days
        assert save._inner_data["Stats_DaysSpent"]["value"] == days

    @pytest.mark.parametrize("deadline", [(1), (2), (3)])
    def test_editing_deadline(self, deadline: int) -> None:
        save = make_save(1)

        assert save.deadline == 3
        assert save.raw_deadline == 3240

        save.update_deadline(deadline)

        assert save.deadline == deadline
        assert save.raw_deadline == deadline * 1080
        assert save._inner_data["DeadlineTime"]["value"] == float(deadline * 1080)

    @pytest.mark.parametrize("quota", [(69), (420), (69420)])
    def test_editing_profit_quota(self, quota: int) -> None:
        save = make_save(2)

        assert save.profit_quota == 220

        save.update_profit_quota(quota)

        assert save.profit_quota == quota
        assert save._inner_data["ProfitQuota"]["value"] == quota

    @pytest.mark.parametrize("progress", [(69), (420), (69420)])
    def test_editing_quota_progress(self, progress: int) -> None:
        save = make_save(1)

        assert save.current_quota_progress == 0

        save.update_current_quota_progress(progress)

        assert save.current_quota_progress == progress
        assert save._inner_data["QuotaFulfilled"]["value"] == progress

    @pytest.mark.parametrize("seed", [(12341234), (56785678), (90129012)])
    def test_editing_seed(self, seed: int) -> None:
        save = make_save(2)

        assert save.current_seed == 24562684

        save.update_current_seed(seed)

        assert save.current_seed == seed
        assert save._inner_data["RandomSeed"]["value"] == seed

    @pytest.mark.parametrize("item", [(ShipUnlock.goldfish), (ShipUnlock.romantic_table), (ShipUnlock.jack_o_lantern)])
    def test_adding_items(self, item: ShipUnlock) -> None:
        save = make_save(1)
        serialised_name = f"ShipUnlockStored_{item.serialised_name}"

        assert item.serialised_value not in save._unlocked_ship_objects["value"]

        save.unlock_ship_upgrades(item)

        assert item.serialised_value in save._unlocked_ship_objects["value"]
        assert serialised_name in save._extra_data

        save.write(dump_to_file=False, overwrite=False)

        assert item.serialised_value in save._inner_data["UnlockedShipObjects"]["value"]
        assert save._inner_data[serialised_name]["value"] is True
