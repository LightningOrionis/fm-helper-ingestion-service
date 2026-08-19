from typing import TypeVar

T = TypeVar("T")


class ItemNotFoundError(Exception):
    def __init__(self, item_type: type[T]) -> None:
        self._item_type = item_type
        super().__init__(f"{self._item_type.__name__} not found")
