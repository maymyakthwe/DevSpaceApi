from pydantic import BaseModel, EmailStr


class Project(BaseModel):
    name: str
    description: str
    techstack: list[str]
    collaborators: list[str]
    commits: int
    highlights: list[str]
    tags: list[str]
    category: str
    type:str
    githubLink:str
    link: str
    active: bool
    isfeatured: bool
    startDate: str
    endDate: str
    status: str


class UserRegister(BaseModel):
    email: EmailStr
    fullname: str
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
    fullname: str
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


class OAuthUser(BaseModel):
    email: str
    fullname: str
    provider: str


class UsernameSetup(BaseModel):
    username: str


class Skill(BaseModel):
    name: str
    category: str
    proficiency: str
    yearsOfExperience: float
    projectRefs: list[str]
    isTopSkill: bool
    icon: str