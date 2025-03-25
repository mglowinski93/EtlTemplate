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


class DataCreationError(Exception):
    pass


class DataAccessError(Exception):
    pass


class FileSaveError(Exception):
    def __init__(self, message: str, file_name: str):
        super().__init__()
        self.message = message
        self.file_name = file_name


class FileNotFoundError(Exception):
    def __init__(self, message: str, file_name: str):
        super().__init__()
        self.message = message
        self.file_name = file_name
