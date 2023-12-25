# pyright: reportPrivateUsage=false
# this is okay in tests


from __future__ import annotations

from pathlib import Path

from great_asset import SaveFile, ShipUnlocks

SAVE_FILE_1 = Path("./save_files/LCSaveFile1")
SAVE_FILE_2 = Path("./save_files/LCSaveFile2")


class TestSaveFile:
    def __init__(self) -> None:
        self.save_file_1 = SaveFile(SAVE_FILE_1)
        self.save_file_2 = SaveFile(SAVE_FILE_2)

    def _reset(self) -> None:
        """Reset the files between each test so we don't lose 'default' data."""
        self.save_file_1 = SaveFile(SAVE_FILE_1)
        self.save_file_2 = SaveFile(SAVE_FILE_2)

    def test_credit_changes(self) -> None:
        # check default values
        assert self.save_file_1.credits == 1605
        assert self.save_file_2.credits == 585

        self.save_file_1.credits = 2820
        self.save_file_2.credits = 312

        self.save_file_1.serialise(write=False)
        assert self.save_file_1._inner_data["GroupCredits"]["value"] == 2820

        self.save_file_2.serialise(write=False)
        assert self.save_file_2._inner_data["GroupCredits"]["value"] == 312

        self._reset()

    def test_adding_teleporter(self) -> None:
        self.save_file_1.unlock_ship_upgrades(ShipUnlocks.teleporter)

        self.save_file_1.serialise(write=False)

        assert (
            ShipUnlocks.teleporter.serialised_value in self.save_file_1._inner_data["UnlockedShipObjects"]["value"]
            and self.save_file_1._inner_data["ShipUnlockStored_Teleporter"]["value"] is True
        )

    def test_removing_teleporter(self) -> None:
        self.save_file_2.unlock_ship_upgrades(ShipUnlocks.teleporter)

        self.save_file_2.remove_ship_upgrades(ShipUnlocks.teleporter)

        self.save_file_2.serialise(write=False)

        assert (
            ShipUnlocks.teleporter.serialised_value not in self.save_file_2._inner_data["UnlockedShipObjects"]["value"]
            and self.save_file_2._inner_data["ShipUnlockStored_Teleporter"]["value"] is False
        )
