from typing import Protocol

from app.enums.fm_import import ImportType, ImportUploadStatus
from app.models.fm_import import Import
from app.models.save import Save


class ImportFactory(Protocol):
    def __call__(  # noqa
        self,
        version: int = 0,
        upload_status: ImportUploadStatus = ImportUploadStatus.STARTED,
        import_type: ImportType = ImportType.SQUAD,
        filename: str = "path/to/file",
        save_id: int | None = None,
    ) -> Import: ...


class SaveFactory(Protocol):
    def __call__(  # noqa
        self,
        name: str = "save",
    ) -> Save: ...
