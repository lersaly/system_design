from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User, Talk, Conference
from database import get_db
from mongodb_service import MongoDBService
from redis_service import RedisCacheService
from passlib.hash import bcrypt
import asyncio
from init_db import init_db

app = FastAPI()
mongodb_service = MongoDBService()
redis_cache_service = RedisCacheService()

@app.on_event("startup")
async def startup_event():
    await init_db()

# Add a method to get conference with Redis caching
@app.get("/conferences/{conference_id}")
async def get_conference(conference_id: int, db: AsyncSession = Depends(get_db)):
    conference = redis_cache_service.get_conference_with_cache(db, conference_id)
    
    if not conference:
        raise HTTPException(status_code=404, detail="Conference not found")
    
    # Log conference access in MongoDB
    mongodb_service.log_conference_activity(
        conference_id, 
        "accessed", 
        {"method": "get_conference"}
    )
    
    return conference

# Additional methods for logging and retrieving MongoDB logs
@app.get("/conferences/{conference_id}/logs")
async def get_conference_logs(conference_id: int):
    logs = mongodb_service.get_conference_logs(conference_id)
    return logs

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the conference app API!"}

@app.post("/users/")
async def create_user(username: str, password: str, db: AsyncSession = Depends(get_db)):
    password_hash = bcrypt.hash(password)
    user = User(username=username, password_hash=password_hash)
    db.add(user)
    await db.commit()
    return {"message": "User created successfully"}

@app.get("/users/{username}")
async def get_user(username: str, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username}

@app.post("/talks/")
async def create_talk(title: str, speaker_id: int, db: AsyncSession = Depends(get_db)):
    talk = Talk(title=title, speaker_id=speaker_id)
    db.add(talk)
    await db.commit()
    return {"message": "Talk created successfully"}

@app.get("/talks/")
async def get_talks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Talk))
    talks = result.scalars().all()
    return [{"id": talk.id, "title": talk.title} for talk in talks]

@app.post("/conferences/{conference_id}/add_talk")
async def add_talk_to_conference(conference_id: int, talk_id: int, db: AsyncSession = Depends(get_db)):
    conference = await db.get(Conference, conference_id)
    talk = await db.get(Talk, talk_id)
    if not conference or not talk:
        raise HTTPException(status_code=404, detail="Conference or talk not found")
    conference.talks.append(talk)
    await db.commit()
    return {"message": "Talk added to conference"}

