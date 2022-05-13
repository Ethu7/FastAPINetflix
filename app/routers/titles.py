from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

from fastapi_pagination import Page, LimitOffsetPage, paginate, Params




router = APIRouter(
    prefix="/titles",
    tags=['Titles']
)



@router.get("/",response_model=Page[schemas.TitleOut])
@router.get("/limit-offset", response_model=LimitOffsetPage[schemas.TitleOut],include_in_schema=False)
def get_titles(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                 limit: int = 10, skip: int = 0, searchTitle: Optional[str] = "", ASC: int = 0,
                 params: Params = Depends()):
    """
    Get all titles from the netflix show database. 
    """

    
    if ASC == 0:
        titles = db.query(models.Title).filter(func.lower(models.Title.title).contains(searchTitle))\
                    .order_by(models.Title.title).limit(limit).offset(skip).all()
    else:
        titles = db.query(models.Title).filter(func.lower(models.Title.title).contains(searchTitle))\
        .order_by(models.Title.title.desc()).limit(limit).offset(skip).all()
    return paginate(titles, params)

   


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Title)
def create_titles(title: schemas.TitleCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Create a new title entry for the Netflix table
    """

    new_title = models.Title(owner_id=current_user.id, **title.dict())
    db.add(new_title)
    db.commit()
    db.refresh(new_title)

    return new_title


@router.get("/{id}", response_model=schemas.TitleOut)
def get_title(id: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Get a single title from the Netflix table
    """
    title = db.query(models.Title).filter(models.Title.show_id == id).first()

    if not title:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Title with id: {id} was not found")

    return title


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_title(id: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Delete a single title from the Netflix table, only if you are the owner of this title.
    """
    title_query = db.query(models.Title).filter(models.Title.show_id == id)

    title = title_query.first()

    if title == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Title with id: {id} does not exist")

    if title.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    title_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Title)
def update_title(id: str, updated_title: schemas.TitleCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Update a single title from the Netflix table, only if you are the owner of this title.
    """

    title_query = db.query(models.Title).filter(models.Title.show_id == id)

    title = title_query.first()

    if title == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Title with id: {id} does not exist")

    if title.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    title_query.update(updated_title.dict(), synchronize_session=False)

    db.commit()

    return title_query.first()
