class DataValidationError(Exception):
    def __init__(self, message: str, file_name: str):
        super().__init__()
        self.message = message
        self.file_name = file_name


class FileExtensionNotSupportedError(Exception):
    def __init__(self, message: str, file_extension: str):
        super().__init__()
        self.message = message
        self.file_extension = file_extension
