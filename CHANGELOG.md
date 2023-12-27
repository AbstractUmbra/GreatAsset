1.1.0

# great_asset Changelog

## Added
- `great_asset.ConfigFile` to support the `LCGeneralSaveFile` that is created on launch, to allow control of the finer details of each player/setup configuration. (87523d5399d2acc2570d967731e5b485bdafdda9)

## Fixed
- Update the GitHub Action to perform the project build on PRs too, to allow contributors to test PRs. (903eefddd795a25e89cfdaf60ae7ed57f049369c)

## Changed
- Moved the primitive inner types of the deserialised files to `types_.shared` instead of `types_.save_file` due to their shared usage. (87523d5399d2acc2570d967731e5b485bdafdda9)
- Added `poethepoet` dev dependency for pre-push CI. (be84c8529fc09121c9a80bd54602794f33d82c11)

### Notes
I'll add some example usage soon.
I'll add a way to edit the other files within the save folder like general config.
The enums still need to be fleshed out and documented, which is slightly tedious.

### Noted Contributors
@sudosnok for their work in deserialising the config file and implementing the base class and config file class.
