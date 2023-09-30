from enum import Enum


class CommandEnum(Enum):
    SET_X = "set_x"
    SET_Y = "set_y"
    RESET = "reset"
    SETUP = "setup"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
