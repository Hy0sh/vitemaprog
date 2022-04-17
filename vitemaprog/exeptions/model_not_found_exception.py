from fastapi import HTTPException

class ModelNotFoundException(HTTPException):
    status_code = 404
    def __init__(self, detail):
        super().__init__(status_code=self.status_code, detail=detail)
