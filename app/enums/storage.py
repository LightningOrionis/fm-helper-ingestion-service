from enum import Enum


class StorageType(str, Enum):
    LOCAL = "local"
    S3 = "s3"
