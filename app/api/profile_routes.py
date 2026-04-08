from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.database import profile_collection, projects_collection
from app.schemas.models import UserProfile
from app.core.security import get_current_user

router = APIRouter()


@router.get("/profile")
async def get_profile(current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]
    profile = await profile_collection.find_one({"userId": user_id})

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile["_id"] = str(profile["_id"])
    return profile


@router.put("/profile/{user_id}")
async def update_profile(user_id: str, updated_data: UserProfile):
    existing_profile = await profile_collection.find_one({"userId": user_id})

    if not existing_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    update_data = updated_data.dict(exclude_unset=True)

    # Prevent changing userId
    update_data.pop("userId", None)

    await profile_collection.update_one({"userId": user_id}, {"$set": update_data})

    updated_profile = await profile_collection.find_one({"userId": user_id})
    updated_profile["_id"] = str(updated_profile["_id"])

    return updated_profile


@router.get("/u/{username}")
async def get_public_profile(username: str):
    # 1. Find the profile directly by username
    profile = await profile_collection.find_one({"username": username})
    
    # 2. If no profile exists OR it isn't marked as public, 404
    if not profile or not profile.get("public", False):
        raise HTTPException(status_code=404, detail="Profile not found or is private")
    
    # Convert MongoDB ObjectId to string for JSON serialization
    profile["_id"] = str(profile["_id"])
    
    # 3. Get their projects using the userId stored in the profile
    # Note: Make sure 'projects_collection' is imported in this file!
    projects = []
    user_id_for_projects = profile.get("userId") 
    
    if user_id_for_projects:
        async for p in projects_collection.find({"userId": user_id_for_projects}):
            p["_id"] = str(p["_id"])
            projects.append(p)

    return {
        "profile": profile,
        "projects": projects
    }







# has not add protected routes
# has not add protected routes
# has not add protected routes
# has not add protected routes
