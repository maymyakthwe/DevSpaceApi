from app.schemas.models import UserRegister, UserLogin, UserProfile, OAuthUser, UsernameSetup
from fastapi import APIRouter, HTTPException, Depends
from app.core.security import create_access_token, hash_password, verify_password, get_current_user
from app.database import user_collection, profile_collection
import uuid
import re
from bson import ObjectId

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user: UserRegister):
    #email unique check
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    #username unique check
    username_check = await user_collection.find_one({"username": user.username})
    if username_check:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    #format check
    import re
    if not re.match(r'^[a-z0-9_-]{3,20}$', user.username):
        raise HTTPException(
            status_code=400,
            detail="Username must be 3-20 characters, lowercase letters, numbers, hyphens, and underscores only"
        )


    # Prepare user data
    data = user.dict()
    data["hash_password"] = hash_password(user.password)
    del data["password"]

    # Insert user
    result = await user_collection.insert_one(data)

    if not result:
        raise HTTPException(status_code=500, detail="User creation failed")

    user_id = str(result.inserted_id)

    # Create profile
    profile = UserProfile(
        fullname=data["fullname"],
        username=data["username"],
        bio="",
        location="",
        email=data["email"],
        portfolio="",
        github="",
        linkedin="",
        twitter="",
        devSpace="",
        about="",
        top_skills=[],
        achievement=[],
        public=True,
        showEmail=False,
        userId=user_id,
    )

    # Insert profile
    await profile_collection.insert_one(profile.dict())

    return {"_id": user_id}


@router.post("/login")
async def login(user: UserLogin):
    db_user = await user_collection.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user["hash_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user["_id"])})

    return {"access_token": token, "token_type": "bearer"}



#for 3rd party oauth login 
@router.post("/oauth")
async def oauth_login(user: OAuthUser):
    db_user = await user_collection.find_one({"email": user.email})

    if not db_user:
        temp_username = f"user_{uuid.uuid4().hex[:8]}"

        data = {
            "email": user.email,
            "fullname": user.fullname,  
            "username": temp_username,  
            "hash_password": None,
            "provider": user.provider,
            "setup_incomplete": True,  
        }
        result = await user_collection.insert_one(data)
        user_id = str(result.inserted_id)

        profile = UserProfile(
            fullname=user.fullname,  
            username=temp_username,
            bio="", location="", email=user.email,
            portfolio="", github="", linkedin="",
            twitter="", devSpace="", about="",
            top_skills=[], achievement=[],
            public=True, showEmail=False, userId=user_id,
        )
        await profile_collection.insert_one(profile.dict())
    else:
        user_id = str(db_user["_id"])

    token = create_access_token({"sub": user_id})
    setup_incomplete = db_user is None or db_user.get("setup_incomplete", False)

    return {
        "access_token": token,
        "token_type": "bearer",
        "setup_incomplete": setup_incomplete
    }


@router.post("/setup-username")
async def setup_username(
    data: UsernameSetup,
    current_user: dict = Depends(get_current_user)
):
    # Validate format
    if not re.match(r'^[a-z0-9_-]{3,20}$', data.username):
        raise HTTPException(
            status_code=400,
            detail="Username must be 3-20 characters, lowercase letters, numbers, hyphens, and underscores only"
        )

    # Check if taken
    existing = await user_collection.find_one({"username": data.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    user_id = current_user["user_id"]

    # Update both user and profile
    await user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"username": data.username, "setup_incomplete": False}}
    )
    await profile_collection.update_one(
        {"userId": user_id},
        {"$set": {"username": data.username}}
    )

    return {"status": "success"}


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "fullname": user.get("fullname", ""),
        "email": user.get("email", ""),
        "username": user.get("username", ""),
    }