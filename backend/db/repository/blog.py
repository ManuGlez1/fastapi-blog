from sqlalchemy.orm import Session
from schemas.blog import BlogCreate, BlogUpdate
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

def list_blogs(db: Session):
    blogs = db.query(Blog).filter(Blog.is_active == True).all()
    return blogs

def update_blog_by_id(id: int, blog: BlogUpdate, db: Session, author_id: int):
    blog_in_db = retrieve_blog(id, db)
    if not blog_in_db:
        return {"error": f"Blog with id {id} does not exist"}
    if not blog_in_db.author_id == author_id:
        return {"error": "Only the author can modify the blog"}
    blog_in_db.title = blog.title
    blog_in_db.content = blog.content
    blog_in_db.slug = blog.slug
    db.add(blog_in_db)
    db.commit()
    return blog_in_db

def delete_blog_by_id(id: int, db: Session, author_id: int):
    blog_in_db = db.query(Blog).filter(Blog.id == id)
    if not blog_in_db.first():
        return {"error": f"Could not find blog with id {id}"}
    if not blog_in_db.first().author_id == author_id:
        return {"error": "Only the author can delete the blog"}
    blog_in_db.delete()
    db.commit()
    return {"msg": f"Deleted blog with id {id}"}