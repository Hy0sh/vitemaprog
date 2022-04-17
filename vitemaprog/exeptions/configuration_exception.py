from fastapi import HTTPException

class ConfigurationException(HTTPException):
    status_code = 500
    def __init__(self, detail):
        super().__init__(status_code=self.status_code, detail=detail)
