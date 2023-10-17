from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # Retrieve the data from the SQL Server
    # Posts with filters, but does not contain votes
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).order_by(models.Post.id).limit(limit).offset(skip).all()

    # To get the posts from the current user 
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # gather the number of votes per post
    votes_qry = db.query(models.Post.id, 
                         func.count(models.Vote.user_id).label("votes")
                         ).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
        ).group_by(models.Post.id).subquery()
        
    posts = db.query(
        models.Post, 
        votes_qry.c.votes
        ).outerjoin(
            votes_qry, 
            models.Post.id == votes_qry.c.id
            ).filter(
                models.Post.title.contains(search)
                ).order_by(
                    models.Post.id
                    ).limit(limit).offset(skip).all()

    return posts

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostNew, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    # Retrieve the posts without votes
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    votes_qry = db.query(models.Post.id, 
                         func.count(models.Vote.user_id).label("votes")
                         ).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True
        ).group_by(models.Post.id).subquery()
        
    post = db.query(
        models.Post, 
        votes_qry.c.votes
        ).outerjoin(
            votes_qry, 
            models.Post.id == votes_qry.c.id
            ).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found.")

    return post

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    #deleting a post
    post_qry = db.query(models.Post).filter(models.Post.id == id)
    post = post_qry.first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"Post with id {id} does not exist.")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = "Not authorized to perform requested action.")
    post_qry.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostNew, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # Update the details of a post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_upd = post_query.first()
    if not post_upd:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"Post with id {id} does not exist.")
    if post_upd.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = "Not authorized to perform requested action.")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
