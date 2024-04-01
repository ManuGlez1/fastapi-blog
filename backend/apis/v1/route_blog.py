from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.blog import BlogCreate, ShowBlog
from db.session import get_db
from db.repository.blog import create_new_blog


router = APIRouter()

@router.post("/", response_model = ShowBlog, status_code = status.HTTP_201_CREATED)
def create_blog(blog: BlogCreate, db: Session = Depends(get_db)):
    blog = create_new_blog(blog = blog, db = db, author_id = 1)
    return blog