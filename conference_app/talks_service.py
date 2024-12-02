from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Talk
from database import get_db
from auth import verify_token
from kafka_service import KafkaService

router = APIRouter()
kafka_service = KafkaService()

class TalkCommand(BaseModel):
    title: str
    description: str
    speaker_id: int

class TalkQuery(BaseModel):
    id: int
    title: str
    description: str
    speaker_id: int

class TalkQueryService:
    @staticmethod
    async def get_talks(db: AsyncSession):
        result = await db.execute(select(Talk))
        talks = result.scalars().all()
        return [
            TalkQuery(
                id=talk.id, 
                title=talk.title, 
                description=talk.description, 
                speaker_id=talk.speaker_id
            ) for talk in talks
        ]
    
    @staticmethod
    async def get_talk_by_id(db: AsyncSession, talk_id: int):
        talk = await db.get(Talk, talk_id)
        if not talk:
            raise HTTPException(status_code=404, detail="Talk not found")
        
        return TalkQuery(
            id=talk.id, 
            title=talk.title, 
            description=talk.description, 
            speaker_id=talk.speaker_id
        )

class TalkCommandService:
    @staticmethod
    async def create_talk(db: AsyncSession, talk_command: TalkCommand):
        talk = Talk(
            title=talk_command.title, 
            description=talk_command.description,
            speaker_id=talk_command.speaker_id
        )
        db.add(talk)
        await db.commit()
        
        # Публикация сообщения в Kafka
        kafka_service.publish_talk_creation({
            'title': talk.title,
            'description': talk.description,
            'speaker_id': talk.speaker_id
        })
        
        return talk

@router.post("/talks")
async def create_talk(
    talk: TalkCommand, 
    token_data: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    new_talk = await TalkCommandService.create_talk(db, talk)
    return {"message": "Talk created successfully", "talk_id": new_talk.id}

@router.get("/talks")
async def get_talks(
    token_data: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    talks = await TalkQueryService.get_talks(db)
    return talks

@router.get("/talks/{talk_id}")
async def get_talk(
    talk_id: int,
    token_data: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    talk = await TalkQueryService.get_talk_by_id(db, talk_id)
    return talk
