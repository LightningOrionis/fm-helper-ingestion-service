from pathlib import Path

from fastapi import UploadFile

from app.config import settings
from app.enums.file import IncorrectFileReason
from app.exceptions.incorrect_file import IncorrectFileError


def non_empty_string_validator(s: str) -> str:
    stripped_s = s.strip()

    if not stripped_s:
        raise ValueError(f"{s} is not a valid string. String should not be empty.")

    return stripped_s


class FileValidator:
    ALLOWED_EXTENSIONS = {".xls", ".xlsx", ".csv"}
    MAX_FILE_SIZE = settings.STORAGE.ALLOWED_FILE_SIZE * 1024 * 1024

    def _validate_size(self, file: UploadFile) -> None:
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        if size > self.MAX_FILE_SIZE:
            raise IncorrectFileError(file.filename, reason=IncorrectFileReason.SIZE)

    def _validate_extension(self, filename: str) -> None:
        extension = Path(filename).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise IncorrectFileError(filename, reason=IncorrectFileReason.EXTENSION)

    def validate(self, file: UploadFile) -> str:
        if not file.filename:
            raise IncorrectFileError(
                file.filename,
                reason=IncorrectFileReason.EXTENSION,
            )
        self._validate_size(file)
        self._validate_extension(file.filename)

        return file.filename
