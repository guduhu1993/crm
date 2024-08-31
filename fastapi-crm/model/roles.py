from pydantic import BaseModel


class RolesInDB(BaseModel):
    id: int
    role_name: str
    role_label: str
    status: bool
    privileges: list[int]


class AddRole(BaseModel):
    role_name: str
    role_label: str
    status: bool
    privileges: list[int]
