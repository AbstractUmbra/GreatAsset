# pyright: reportPrivateUsage=false
# this is okay in tests


from __future__ import annotations

from pathlib import Path
from typing import Literal

from great_asset import SaveFile, ShipUnlock

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
