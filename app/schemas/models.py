from pydantic import BaseModel, EmailStr


class Project(BaseModel):
    name: str
    description: str
    techstack: list[str]
    lastUpdated: str
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


class UserProfile(BaseModel):
    username: str
    bio: str
    location: str
    email: EmailStr
    portfolio: str
    github: str
    linkedin: str
    twitter: str
    devSpace: str
    about: str
    top_skills: list[str]
    achievement: list[str]
    public: bool
    showEmail: bool
    userId: str
