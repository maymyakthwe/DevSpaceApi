from pydantic import BaseModel, EmailStr


class Project(BaseModel):
    name: str
    description: str
    status: str
    techstack: list[str]
    lastUpdated: str
    progress: int
    link: str
    active: bool


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
