from sqlalchemy.orm import Session
from schemas.blog import BlogCreate
from db.models.blog import Blog


def create_new_blog(blog: BlogCreate, db: Session, author_id: int = 1):
    blog = Blog(
       title = blog.title,
       slug = blog.slug,
       content = blog.content,
       author_id = author_id
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

def retrieve_blog(id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    return blog