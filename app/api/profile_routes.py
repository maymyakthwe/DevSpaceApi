from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.database import profile_collection
from app.schemas.models import UserProfile
from app.core.security import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/")
async def get_profile(current_user=Depends(get_current_user)):
    user_id = current_user["user_id"]
    profile = await profile_collection.find_one({"userId": user_id})

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile["_id"] = str(profile["_id"])
    return profile


@router.put("/{user_id}")
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


# has not add protected routes
