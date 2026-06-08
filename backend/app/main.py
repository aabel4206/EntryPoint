from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routes import resources

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(resources.router)


@app.get("/")
def root():
    return {"message": "EntryPoint API is running"}