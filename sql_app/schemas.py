from pydantic import BaseModel


class Employee(BaseModel):
    id: int
    FirstName: str
    LastName: str
    Address: str
    City: str
    State: str
    ZIP: int

    class Config:
        orm_mode = True


class Emp(Employee):
    hashed_password: str

    class Config:
        orm_mode = True
