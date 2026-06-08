from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models, schemas

router = APIRouter(
    prefix="/api/resources",
    tags=["Resources"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/categories", response_model=list[schemas.ResourceCategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.ResourceCategory).all()


@router.post("/categories", response_model=schemas.ResourceCategoryResponse)
def create_category(category: schemas.ResourceCategoryCreate, db: Session = Depends(get_db)):
    new_category = models.ResourceCategory(
        name=category.name,
        description=category.description
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/", response_model=list[schemas.ResourceResponse])
def get_resources(db: Session = Depends(get_db)):
    return db.query(models.Resource).all()


@router.post("/", response_model=schemas.ResourceResponse)
def create_resource(resource: schemas.ResourceCreate, db: Session = Depends(get_db)):
    category = db.query(models.ResourceCategory).filter(
        models.ResourceCategory.category_id == resource.category_id
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    new_resource = models.Resource(
        category_id=resource.category_id,
        title=resource.title,
        description=resource.description,
        url=resource.url
    )

    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)

    return new_resource