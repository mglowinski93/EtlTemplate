class TypeNotSupportedError(Exception):
    def __init__(self, file_format: str):
        self.file_format = file_format
        super().__init__(self)
    
    def __str__(self):
        return f"File format not supported {self.file_format}"
