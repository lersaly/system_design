from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from auth import verify_token

router = APIRouter()

class Talk(BaseModel):
    title: str
    description: str

talks_db = {}

@router.post("/talks")
def create_talk(talk: Talk, token_data: dict = Depends(verify_token)):
    talk_id = len(talks_db) + 1
    talks_db[talk_id] = {"title": talk.title, "description": talk.description}
    return {"message": "Talk created successfully", "talk_id": talk_id}

@router.get("/talks")
def get_all_talks(token_data: dict = Depends(verify_token)):
    return talks_db