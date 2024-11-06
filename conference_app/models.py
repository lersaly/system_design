from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)  # Обязательное поле
    password_hash = Column(String, nullable=False)  # Обязательное поле

class Talk(Base):
    __tablename__ = "talks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False) 
    speaker_id = Column(Integer, ForeignKey("users.id"))
    speaker = relationship("User")

class Conference(Base):
    __tablename__ = "conferences"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False) 
    talks = relationship("Talk", secondary="conference_talk_link")

# Вспомогательная таблица для связи "многие ко многим" между конференциями и докладами
conference_talk_link = Table(
    "conference_talk_link", Base.metadata,
    Column("conference_id", Integer, ForeignKey("conferences.id"), primary_key=True),
    Column("talk_id", Integer, ForeignKey("talks.id"), primary_key=True)
)



