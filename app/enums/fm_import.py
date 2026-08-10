from enum import Enum


class ImportType(str, Enum):
    SQUAD = "squad"
    SHORTLIST = "shortlist"


class ImportUploadStatus(str, Enum):
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    FAILED = "failed"
    COMPLETED = "completed"
