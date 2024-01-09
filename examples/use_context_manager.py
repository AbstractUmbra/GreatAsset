"""
This example showcases the use of the class' `__enter__` and `__exit__` methods.
When calling `__exit__` (when you leave the context manager), the edited data is written to the save as if you called `.write()` manually.
"""

from great_asset import SaveFile, Scrap, Vector


def main(save_path: str) -> None:
    with SaveFile(save_path) as save:
        save.update_credits(9999)
        save.spawn_items((Scrap.shotgun, None), (Scrap.shotgun_shell, Vector.in_cupboard()))
        save.update_deadline(8)
        save.update_steps_taken(69)


if __name__ == "__main__":
    main("/path/to/save")
