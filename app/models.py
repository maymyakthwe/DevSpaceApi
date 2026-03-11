from pydantic import BaseModel


class Project(BaseModel):
    name: str
    description: str
    status: str
    techstack: list[str]
    lastUpdated: str
    progress: int
    link: str
    active: bool
