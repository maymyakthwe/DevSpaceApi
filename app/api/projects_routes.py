from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database import projects_collection
from app.schemas.models import Project

router = APIRouter(prefix="/projects", tags=["Download"])


@router.post("/")
def create_project(project: Project):
    data = project.dict()
    result = projects_collection.insert_one(data)
    return {"_id": str(result.inserted_id)}


@router.get("/")
def get_projects():
    projects = []
    for p in projects_collection.find():
        p["_id"] = str(p["_id"])
        projects.append(p)
    return projects


@router.get("/{id}")
def get_one(id: str):
    project = projects_collection.find_one({"_id": ObjectId(id)})

    if project is None:
        raise HTTPException(status_code=404, detail="project not found")

    project["_id"] = str(project["_id"])
    return project


@router.put("/{id}")
def update_project(id: str, project: Project):
    projects_collection.update_one({"_id": ObjectId(id)}, {"$set": project.dict()})
    return {"message": "updated"}


@router.delete("/{id}")
def delete_project(id: str):
    projects_collection.delete_one({"_id": ObjectId(id)})
    return {"message": "deleted"}
