from app.schemas.models import UserRegister, UserResponse, UserLogin
from fastapi import APIRouter, HTTPException
from app.core.security import create_access_token, hash_password, verify_password
from app.database import user_collection

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user: UserRegister):
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    data = user.dict()
    data["hash_password"] = hash_password(user.password)
    del data["password"]
    result = await user_collection.insert_one(data)
    return {"_id": str(result.inserted_id)}


@router.post("/login")
async def login(user: UserLogin):
    db_user = await user_collection.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user["hash_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user["_id"])})

    return {"access_token": token, "token_type": "bearer"}
