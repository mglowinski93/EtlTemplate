class DatabaseError(Exception):
    def __init__(self, message: str,):
        super().__init__(message)

class DataDoesNotExist:
    def __init__(self, message: str,):
        super().__init__(message)    
