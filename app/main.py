from fastapi import FastAPI

from app.routes.auth_routes import router as auth_router
from app.database.database import Base, engine
from app.database.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "Chat app backend is running!"}