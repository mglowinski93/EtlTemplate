class FileTypeNotSupportedErrod(Exception):
    def __init__(self, file_format: str):
        self.file_format = file_format
        super().__init__(self)

    
class FileNotFoundError(Exception):
    def __init__(self, file_path: str):
        self.file_path = file_path
        super().__init__(self)
