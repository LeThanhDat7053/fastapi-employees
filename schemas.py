from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    name: str
    position: str
