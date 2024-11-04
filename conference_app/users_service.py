from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from utils import hash_password, verify_password
import asyncpg

app = FastAPI()

DATABASE_URL = "postgresql://postgres:postgres@db/conference_app"

async def get_db_pool():
    return await asyncpg.create_pool(DATABASE_URL)

class User(BaseModel):
    username: str
    password: str

@app.post("/users/", response_model=User)
async def create_user(user: User):
    pool = await get_db_pool()
    async with pool.acquire() as connection:
        password_hash = hash_password(user.password)  # Используем хеширование пароля
        await connection.execute('''
            INSERT INTO users (username, password_hash) VALUES ($1, $2)
        ''', user.username, password_hash)
    return user

@app.get("/users/{username}", response_model=User)
async def read_user(username: str):
    pool = await get_db_pool()
    async with pool.acquire() as connection:
        user = await connection.fetchrow('SELECT * FROM users WHERE username = $1', username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return User(username=user['username'], password="")  # Не возвращаем пароль

@app.put("/users/{username}", response_model=User)
async def update_user(username: str, user: User):
    pool = await get_db_pool()
    async with pool.acquire() as connection:
        password_hash = some_hashing_function(user.password)  # Реализуйте хеширование пароля
        await connection.execute('''
            UPDATE users SET username = $1, password_hash = $2 WHERE username = $3
        ''', user.username, password_hash, username)
        return user

@app.delete("/users/{username}")
async def delete_user(username: str):
    pool = await get_db_pool()
    async with pool.acquire() as connection:
        await connection.execute('DELETE FROM users WHERE username = $1', username)
        return {"detail": "User deleted"}

