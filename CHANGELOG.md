1.1.3

# great_asset Changelog

## Added
- Finalised the `ShipUnlock` enum (as of game ver .45). (db253f92547ff96a36c2ed78c55524682480d5e1)
- Some examples. (174002ba8ddcb67d595061f3ae1144cad7e1d468)
- `_BaseSaveFile.__enter__`/`__exit__` for ease of use, and relevant example. (6d708964adde1eacb3ab87e2db231069050cccae and 174002ba8ddcb67d595061f3ae1144cad7e1d468 and 1c042541f61a763bc7b00f5e3b137198cadd3246)
- `_BaseSaveFile.from_data` classmethod to allow creation of an object from the raw `bytes` rather than a `Path`. (d576be089f7f76fb18016a08bf5ff61a13cd14b8)

## Fixed
- The way in which we spawn items. (04963a38cacb8d1a2a3223367b0ba6df800a7b50)
  - This likely deserves a post of it's own but the tl;dr is that items on the ship are directly `zip`able with the scrap values key.

## Changed
- Some `Item`s were split into the `Scrap` enum for better separation of item/scrap. (3d4b3309125c2004744b772699e5b86f32284966)
- `Vector.on_cupboard` -> `Vector.in_cupboard`. (3ee802b61d54459cdab819f3d4322a98fa20b726)
- `Vector.default` and `Vector.in_cupboard`'s `x` value was a little askew. (092e61a63943b61fa7583723995ba72222b687e4 and 92579775a159e2e7426386b29fe44d2a6f357e00)
- Removed `SaveFile`'s `__init__` so that the base class' is utilised. (ee7bab52df5beabee9cdccb5713306926dbdcdd6)

### Notes

### Noted Contributors
