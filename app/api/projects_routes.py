from app.core.security import get_current_user
from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.database import projects_collection
from app.schemas.models import Project

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/")
async def create_project(project: Project, current_user=Depends(get_current_user)):
    data = project.dict()
    data["userId"] = current_user["user_id"]  
    result = await projects_collection.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return data


@router.get("/")
async def get_projects(current_user=Depends(get_current_user)):
    projects = []
    async for p in projects_collection.find({"userId": current_user["user_id"]}):
        p["_id"] = str(p["_id"])
        projects.append(p)
    return projects


@router.get("/{id}")
async def get_one(id: str, current_user=Depends(get_current_user)):
    project = await projects_collection.find_one({
        "_id": ObjectId(id),
        "userId": current_user["user_id"] 
    })
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    project["_id"] = str(project["_id"])
    return project


@router.put("/{id}")
async def update_project(id: str, project: Project, current_user=Depends(get_current_user)):
    existing = await projects_collection.find_one({
        "_id": ObjectId(id),
        "userId": current_user["user_id"]  
    })
    if not existing:
        raise HTTPException(status_code=404, detail="Project not found")

    await projects_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": project.dict()}
    )
    return {"message": "updated"}


@router.delete("/{id}")
async def delete_project(id: str, current_user=Depends(get_current_user)):
    existing = await projects_collection.find_one({
        "_id": ObjectId(id),
        "userId": current_user["user_id"]  
    })
    if not existing:
        raise HTTPException(status_code=404, detail="Project not found")

    await projects_collection.delete_one({"_id": ObjectId(id)})
    return {"message": "deleted"}