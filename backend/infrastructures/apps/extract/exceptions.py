class FileSaveError(Exception):
    def __init__(self, message: str, file_name: str):
        super().__init__()
        self.file_name = file_name
