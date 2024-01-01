1.1.0

# great_asset Changelog

## Added
- More tests around the library. (7b4f562bcfe3755095f02aca18dd585306200176)
- Update the in-memory `SaveFile` as well as the serialisation object. (9e19214c76bf600080a57ed405c8f1f2ae177fab)
- More `ShipUnlock` ids and one `ExtraUnlock` id. (bfde042c92e5990a77c6451eb2c03fcba8d12a78)

## Fixed
- Update usage and setting of `SaveFile.deadline` and added `SaveFile.raw_deadline`. (4b9d9142f9ec77420df3f45efe18db4400dcb219 and c4f263886c5d299d4a1466498ad59a02aa1de149)
  - The save file uses the minute value per day as the setting. E.g. 1 day is 1080 serialised.
- Fixed a typo in `SaveFile.update_elapsed_days`. (1c3fcf59e79730c42670019ffe61b0986e7b568d)
## Changed


### Notes
I'll add some example usage soon.
I'll add a way to edit the other files within the save folder like general config.
The enums still need to be fleshed out and documented, which is slightly tedious.

### Noted Contributors
