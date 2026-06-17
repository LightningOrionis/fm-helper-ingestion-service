from enum import Enum

class StorageTypeEnum(str, Enum):
    LOCAL = "local"
    S3 = "s3"
