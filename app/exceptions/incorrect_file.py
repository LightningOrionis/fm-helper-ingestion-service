from app.enums.file import IncorrectFileReason

REASONING = {
    IncorrectFileReason.SIZE: "File size is too large.",
    IncorrectFileReason.EXTENSION: "File extensions supported: csv, xls, xlsx.",
}


class IncorrectFileError(ValueError):
    def __init__(self, filename: str | None, reason: IncorrectFileReason) -> None:
        self._filename = filename
        self._reasoning = REASONING[reason]
        super().__init__(f"{self._filename} is incorrect. {self._reasoning}")
