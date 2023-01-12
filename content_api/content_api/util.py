import json
import math
from numbers import Number
from typing import Callable

def sum_values_of_key(options: dict, key: object) -> Number:
    return sum([option[key] for option in options])

def seconds_to_hours(seconds: int) -> int:
    return math.floor(seconds / 3600)

def seconds_to_hourminutes(seconds: int) -> int:
    return math.floor((seconds % 3600) / 60)
    


class PersistentObject:
    def __init__(self, path: str, 
                 on_load: Callable[[str], object] = None,
                 on_write: Callable[[object], str] = None) -> None:
        self._data_path = path
        self._value = None
        if on_load is None:
            on_load = lambda x: x
        self._on_load = on_load
        if on_write is None:
            on_write = lambda x: x
        self._on_write = on_write

    def set(self, new_value: object):
        self._value = new_value
        with open(self._data_path, "w+", encoding="utf-8") as data_file:
            written_value = self._on_write(new_value)
            data_file.write(written_value)

    def get(self) -> object:
        if self._value is None:
            self._load_from_disk()
        return self._value

    def is_defined(self) -> bool:
        if self._value is None:
            self._load_from_disk()
        return not self._value is None

    def _load_from_disk(self):
        try:
            with open(self._data_path, "r", encoding="utf-8") as data_file:
                data = data_file.read()
            self._value = self._on_load(data)
        except:
            self._value = None

class PersistentDict(PersistentObject):
    def __init__(self, path: str):
        super().__init__(path, 
            on_load=lambda x: json.loads(x),
            on_write=lambda x: json.dumps(x))
