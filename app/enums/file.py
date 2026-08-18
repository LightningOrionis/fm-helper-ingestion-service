from enum import Enum


class IncorrectFileReason(str, Enum):
    SIZE = "size"
    EXTENSION = "extension"
