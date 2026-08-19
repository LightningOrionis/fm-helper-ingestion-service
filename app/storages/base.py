from abc import ABC, abstractmethod
from typing import BinaryIO


class BaseStorage(ABC):

    @abstractmethod
    def _generate_filepath(self, filename: str) -> str: ...  # noqa: E704

    @abstractmethod
    def _save_file(self, file: BinaryIO, path_to_file: str) -> None: ...  # noqa: E704

    @abstractmethod
    def upload_file(self, file: BinaryIO, filename: str) -> str: ...  # noqa: E704

    @abstractmethod
    def delete_file(self, filename: str) -> None: ...  # noqa: E704
