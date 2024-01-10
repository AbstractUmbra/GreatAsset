"""
This example will showcase how to spawn items on the ship. This has to be done when the ship is in orbit as that is when the save is written.
Items and Scrap are separated into `great_asset.Scrap` and `great_asset.Item`. The method for spawning is the same for both types.
"""

from great_asset import Item, SaveFile, Vector


def main(save_path: str) -> None:
    save = SaveFile.from_path(save_path)

    # let's say we want to spawn in the "explorer toolkit" (4x shovel, walkie and flashlight)
    # we can define the items and their spawn positions in a tuple format:-
    items = [
        (Item.pro_flashlight, Vector.in_cupboard()),
        (Item.pro_flashlight, Vector.in_cupboard()),
        (Item.pro_flashlight, Vector.in_cupboard()),
        (Item.pro_flashlight, Vector.in_cupboard()),
        (Item.walkie_talkie, Vector.in_cupboard()),
        (Item.walkie_talkie, Vector.in_cupboard()),
        (Item.walkie_talkie, Vector.in_cupboard()),
        (Item.walkie_talkie, Vector.in_cupboard()),
        (Item.shovel, Vector.in_cupboard()),
        (Item.shovel, Vector.in_cupboard()),
        (Item.shovel, Vector.in_cupboard()),
        (Item.shovel, Vector.in_cupboard()),
    ]
    # the `Vector.in_cupboard()` method will create a position within the cupboard in it's default spawn location.

    save.spawn_items(*items)


if __name__ == "__main__":
    main("/path/to/save")
