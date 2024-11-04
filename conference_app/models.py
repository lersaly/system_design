from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Базовый класс для всех моделей
Base = declarative_base()

# Модель User
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

# Модель Talk
class Talk(Base):
    __tablename__ = "talks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    speaker_id = Column(Integer, ForeignKey("users.id"))
    speaker = relationship("User")

# Модель Conference
class Conference(Base):
    __tablename__ = "conferences"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    talks = relationship("Talk", secondary="conference_talk_link")

# Вспомогательная таблица для связи "многие ко многим" между конференциями и докладами
conference_talk_link = Table(
    "conference_talk_link", Base.metadata,
    Column("conference_id", Integer, ForeignKey("conferences.id"), primary_key=True),
    Column("talk_id", Integer, ForeignKey("talks.id"), primary_key=True)
)


