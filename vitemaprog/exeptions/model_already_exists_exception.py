from fastapi import HTTPException

class ModelAlreadyExistsException (HTTPException):
    status_code = 400
    def __init__(self, detail):
        super().__init__(status_code=self.status_code, detail=detail)
