from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database import projects_collection
from app.schemas.models import Project

router = APIRouter(prefix="/projects", tags=["Download"])


@router.post("/")
async def create_project(project: Project):
    data = project.dict()
    result = await projects_collection.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return data


@router.get("/")
async def get_projects():
    projects = []

    async for p in projects_collection.find():
        p["_id"] = str(p["_id"])
        projects.append(p)

    return projects


@router.get("/{id}")
async def get_one(id: str):
    project = await projects_collection.find_one({"_id": ObjectId(id)})

    if project is None:
        raise HTTPException(status_code=404, detail="project not found")

    project["_id"] = str(project["_id"])
    return project


@router.put("/{id}")
async def update_project(id: str, project: Project):
    await projects_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": project.dict()}
    )
    return {"message": "updated"}


@router.delete("/{id}")
async def delete_project(id: str):
    await projects_collection.delete_one({"_id": ObjectId(id)})
    return {"message": "deleted"}
