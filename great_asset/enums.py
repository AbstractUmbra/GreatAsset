"""
The MIT License (MIT)

Copyright (c) 2023-present AbstractUmbra

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from enum import Enum

__all__ = (
    "ShipUnlock",
    "ExtraUnlock",
    "BestiaryEntry",
    "Item",
    "Moon",
)


class ShipUnlock(Enum):
    signal_translator = 0, "Signal translator"
    signal_transmitter = 0, "Signal translator"
    teleporter = 5, "Teleporter"
    television = 6, "Television"
    tv = 6, "Television"
    # = 7
    bunkbeds = 8, "Bunkbeds"  # maybe?
    shower = 10, "Shower"
    file_cabinet = 11, "File Cabinet"  # maybe?
    table = 13, "Table"
    romantic_table = 14, "Romantic table"
    # = 15
    loud_horn = 18, "Loud horn"
    inverse_teleporter = 19, "Inverse Teleporter"
    jack_o_lantern = 20, "JackOLantern"
    goldfish = 22, "Goldfish"
    plushie_pajama_man = 23, "Plushie pajama man"
    plushie_pyjama_man = 23, "Plushie pajama man"

    def __init__(self, value: int, serialised_name: str) -> None:
        self._serialised_value: int = value
        self._serialised_name: str = serialised_name

    @property
    def serialised_value(self) -> int:
        return self._serialised_value

    @property
    def serialised_name(self) -> str:
        return self._serialised_name

    @staticmethod
    def all() -> list["ShipUnlock"]:
        return list(ShipUnlock)


class ExtraUnlock(Enum):
    green_suit = 1
    hazard_suit = 2
    pyjama_suit = 3

    @staticmethod
    def all() -> list["ExtraUnlock"]:
        return list(ExtraUnlock)


class BestiaryEntry(Enum):
    snare_flea = 0
    bracken = 1
    thumper = 2
    eyeless_dog = 3
    hoarding_bug = 4
    hygroderes = 5
    slime = 5
    forest_keepers = 6
    giants = 6
    coil_head = 7
    spring_head = 7
    lasso_man = 8  # not implemented?
    earth_leviathan = 9
    sand_worm = 9
    jester = 10
    jack_in_the_box = 10
    spore_lizard = 11  # not implemented?
    bunker_spider = 12
    spider = 12
    manticoil = 13
    circuit_bees = 14
    bees = 14
    roaming_locusts = 15
    locusts = 15
    baboon_hawk = 16
    nutcracker = 17

    @staticmethod
    def all() -> list["BestiaryEntry"]:
        return list(BestiaryEntry)


class Item(Enum):
    binoculars = 0  # not yet implemented
    boom_box = 1
    flashlight = 3
    jetpack = 4
    key = 5
    lockpick = 6
    apparatus = 7
    handheld_monitor = 8  # not yet implemented
    pro_flashlight = 9
    shovel = 10
    flashbang = 11
    extension_ladder = 12
    tzp_inhalant = 13
    walkie_talkie = 14
    stun_gun = 15
    magic_7_ball = 16
    airhorn = 17
    bell = 18
    big_bolt = 19
    bottles = 20
    hairbrush = 21
    candy = 22
    cash_register = 23
    chemical_jug = 24
    clown_horn = 25
    large_axel = 26
    teeth = 27
    dustpan = 28
    egg_beater = 29
    v_type_engine = 30
    golden_cup = 31
    lamp = 32
    painting = 33
    plastic_fish = 34
    laser_pointer = 35
    gold_bar = 36
    hairdryer = 37
    magnifying_glass = 38
    tattered_metal_sheet = 39
    cookie_mold_pan = 40
    coffee_mug = 41
    perfume_bottle = 42
    old_phone = 43
    jar_of_pickles = 44
    pill_bottle = 45
    ring = 47
    robot_toy = 48
    rubber_ducky = 49
    red_soda = 50
    steering_wheel = 51
    stop_sign = 52
    tea_kettle = 53
    toothpaste = 54
    toy_cube = 55
    bee_hive = 56
    radar_booster = 57
    yield_sign = 58
    shotgun = 59
    shotgun_shell = 60
    spray_paint = 61
    homemade_flashbang = 62
    gift_box = 63
    flask = 64
    tragedy = 65
    comedy = 66
    whoopie_cushion = 67


class Moon(Enum):
    experimentation = 0
    assurance = 1
    vow = 2
    company_building = 3
    march = 4
    rend = 5
    dine = 6
    offense = 7
    titan = 8
