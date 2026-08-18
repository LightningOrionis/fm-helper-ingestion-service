from pathlib import Path
from typing import BinaryIO

from app.config import settings

from .base import BaseStorage


class LocalStorage(BaseStorage):
    def _generate_filepath(self, filename: str) -> str:
        return str(Path(settings.STORAGE.FILE_PATH) / filename)

    def _save_file(self, file: BinaryIO, path_to_file: str) -> None:
        with open(path_to_file, "wb") as destination:
            destination.write(file.read())

    def upload_file(self, file: BinaryIO, filename: str) -> str:
        path_to_file = self._generate_filepath(filename)
        self._save_file(file, path_to_file)

        return path_to_file

    def delete_file(self, filename: str) -> None:
        path_to_file = self._generate_filepath(filename)
        Path(path_to_file).unlink(missing_ok=True)
