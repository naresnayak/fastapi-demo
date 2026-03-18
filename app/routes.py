from fastapi import APIRouter, Depends
from .models import User, UserResponse
from .database import db
from bson import ObjectId

router = APIRouter()

# 1. Define a dependency to get the users collection
def get_users_collection():
    return db.users

@router.post("/users", response_model=UserResponse)
async def create_user(user: User, collection = Depends(get_users_collection)):
    # 2. Use the injected collection instead of the global 'db'
    # Using model_dump() is preferred in Pydantic v2 [cite: 2]
    user_data = user.dict() 
    new_user = await collection.insert_one(user_data)
    return {**user_data, "id": str(new_user.inserted_id)}

@router.get("/users")
async def get_users(collection = Depends(get_users_collection)):
    users = []
    # 3. Use the injected collection for the find operation
    async for user in collection.find():
        user["id"] = str(user.pop("_id"))
        users.append(user)
    return users