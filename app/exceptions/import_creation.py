class ImportCreationError(Exception):
    def __init__(self):
        super().__init__("Failed to create import")
