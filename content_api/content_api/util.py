from numbers import Number

def sum_values_of_key(options: dict, key: object) -> Number:
    return sum([option[key] for option in options])
