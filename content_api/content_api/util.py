import math
from numbers import Number


def sum_values_of_key(options: dict, key: object) -> Number:
    return sum([option[key] for option in options])

def seconds_to_hours(seconds: int) -> int:
    return math.floor(seconds / 3600)

def seconds_to_hourminutes(seconds: int) -> int:
    return math.floor((seconds % 3600) / 60)
    