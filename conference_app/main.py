from fastapi import FastAPI
import uvicorn
from users_service import router as users_router
from talks_service import router as talks_router

app = FastAPI()

app.include_router(users_router, prefix="/users")
app.include_router(talks_router, prefix="/conference")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
