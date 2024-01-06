1.1.2

# great_asset Changelog

## Added
- `SaveFile.resolve_from_file` was added to load the save files from the default (Windows) save file paths. (4797b259c05a4ebcb1385e3f974e4be6f09507e0 and 01f0a35d8f60d4f7237af0b8509082903846215f)
- `Vector.in_cupboard` was added to provide a random place in the default cupboard location for item spawning. (2db2cc92dd6a325536b7ab319bfce60646ecd4c4)
- `BestiaryEntry` enum and `SaveFile.unlock_(all_)bestiary_entries` methods were added to allow control over these unlocks. (17ae5e81d71723f3b945ecd2ef2cf93d40ff2735)

## Fixed
- Corrected the inner type information on the save file structure. (90518841be74dfd9f0b9fa3fe22ba1fe044619ac)
  - This is not part of the public API and should not be relied on.
- Corrected the serialised name for the signal transmitter/locator. (39fbfae5cb249c51c176003b9efd987b89c607cf)
- The default `Vector` location was in the middle of the wall at the bunkbeds, this has now been fixed. (2db2cc92dd6a325536b7ab319bfce60646ecd4c4)
- Enemy scan data was missed during serialisation, this has now been corrected. (17ae5e81d71723f3b945ecd2ef2cf93d40ff2735)

## Changed


### Notes


### Noted Contributors
