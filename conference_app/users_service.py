from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from auth import create_access_token, verify_token

router = APIRouter()

class User(BaseModel):
    username: str
    full_name: str
    password: str

users_db = {
    "admin": {"username": "admin", "full_name": "Administrator", "password": "secret"}
}

@router.post("/register")
def register_user(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.username] = {
        "username": user.username,
        "full_name": user.full_name,
        "password": user.password,
    }
    return {"message": "User registered successfully"}

@router.post("/token")
def login(user: User):
    if user.username not in users_db or users_db[user.username]["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
def get_current_user(token_data: dict = Depends(verify_token)):
    username = token_data.get("sub")
    if username is None or username not in users_db:
        raise HTTPException(status_code=401, detail="Invalid token")
    return users_db[username]
