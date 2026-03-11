from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database import collection
from app.models import Project

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Hello World"}


@router.post("/projects")
def create_project(project: Project):
    data = project.dict()
    result = collection.insert_one(data)
    return {"_id": str(result.inserted_id)}


@router.get("/projects")
def get_projects():
    projects = []
    for p in collection.find():
        p["_id"] = str(p["_id"])
        projects.append(p)
    return projects


@router.get("/projects/{id}")
def get_one(id: str):
    project = collection.find_one({"_id": ObjectId(id)})

    if project is None:
        raise HTTPException(status_code=404, detail="project not found")

    project["_id"] = str(project["_id"])
    return project


@router.put("/projects/{id}")
def update_project(id: str, project: Project):
    collection.update_one({"_id": ObjectId(id)}, {"$set": project.dict()})
    return {"message": "updated"}


@router.delete("/projects/{id}")
def delete_project(id: str):
    collection.delete_one({"_id": ObjectId(id)})
    return {"message": "deleted"}
