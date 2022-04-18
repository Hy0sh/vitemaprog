
from fastapi import HTTPException


class ValidationException(HTTPException):
    status_code = 422
    def __init__(self, message: str, type: str, field: str):
        detail = {
            'loc': [
                'body',
                field
            ],
            'msg': message,
            'type': type
        }
        super().__init__(status_code=self.status_code, detail=detail)
