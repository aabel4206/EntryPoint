from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routes import resources
from app.routes import checklists
from app.routes import monitoring

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EntryPoint API",
    description="Backend API for the EntryPoint personalized onboarding framework.",
    version="1.0.0"
)

app.include_router(resources.router)
app.include_router(checklists.router)
app.include_router(monitoring.router)


@app.get("/")
def root():
    return {"message": "EntryPoint API is running"}