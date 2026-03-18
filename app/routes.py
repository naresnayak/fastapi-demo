from fastapi import APIRouter
from .models import User, UserResponse
from .database import db
from bson import ObjectId

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create_user(user: User):
    new_user = await db.users.insert_one(user.dict())
    return {**user.dict(), "id": str(new_user.inserted_id)}

@router.get("/users")
async def get_users():
    users = []
    async for user in db.users.find():
        user["id"] = str(user.pop("_id"))
        users.append(user)
    return users