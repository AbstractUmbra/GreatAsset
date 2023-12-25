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
    "ShipUnlocks",
    "Items",
    "Planets",
)


class ShipUnlocks(Enum):
    teleporter = 5
    inverse_teleporter = 19


class Items(Enum):
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


class Planets(Enum):
    experimentation = 0
    assurance = 1
    vow = 2
    company_building = 3
    march = 4
    rend = 5
    dine = 6
    offense = 7
    titan = 8
