<div align="center">
    <h1 align="center">
        <b>GreatAsset</b>
        <br>
    </h1>
    <a href='https://github.com/AbstractUmbra/great_asset/actions/workflows/build.yaml'>
        <img src='https://github.com/AbstractUmbra/great_asset/actions/workflows/build.yaml/badge.svg' alt='Build status'/>
    </a>
    <a href='https://github.com/AbstractUmbra/great_asset/workflows/coverage_and_lint.yaml'>
        <img src='https://github.com/AbstractUmbra/great_asset/actions/workflows/coverage_and_lint.yaml/badge.svg' alt='Linting and Typechecking'/>
    </a>
</div>
<div align="center">
    <a href='https://great-asset.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/great_asset/badge/?version=latest' alt='Documentation Status'/>
    </a>
    <a href="https://discord.gg/aYGYJxwqe5">
        <img src='https://img.shields.io/discord/705500489248145459?color=blue&label=Discord&logo=Discord%20Server&logoColor=green' alt='Discord Server'>
    </a>
</div>
<br>

Welcome, great assets to The Company!

---

This project is a small thin wrapper to edit save files for the [Lethal Company](https://store.steampowered.com/app/1966720/Lethal_Company/) video game.

Our documentation can be found [here](https://great-asset.readthedocs.io/en/latest/index.html).

## Example usage

Add 6000 credits and unlock all possible (found) ship upgrades.

```py
import os
import pathlib

import great_asset

SAVE_FILE_LOCATION = pathlib.Path(os.getenv("USERPROFILE")) / "AppData" / "LocalLow" / "ZeekerssRBLX" / "Lethal Company"
SAVE_FILE_1 = SAVE_FILE_LOCATION / "LCSaveFile1"

def main() -> None:
    save = great_asset.SaveFile(SAVE_FILE_1)

    # update credits to 6000
    save.update_credits(6000)

    # unlock all items within `great_asset.ShipUnlock` enum.
    save.unlock_all_ship_upgrades()

    # serialise the data we changed to the save file format
    # and dump & overwrite the passed save file above.
    save.write()
```


## Disclaimer

This project is not affiliated with Lethal Company, [its creator](https://store.steampowered.com/search/?developer=Zeekerss&snr=1_5_9__2000) or affiliates in any way.
Use of this project within public games without players consent is likely going to remove a lot of the fun from the game and is discouraged.
