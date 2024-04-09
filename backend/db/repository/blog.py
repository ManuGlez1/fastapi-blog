from sqlalchemy.orm import Session
from schemas.blog import BlogCreate, BlogUpdate
from db.models.blog import Blog
from core.config import settings
import redis


r = redis.StrictRedis(host = settings.REDIS_HOST, port = settings.REDIS_PORT, decode_responses = True)


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
    r.hset(
        f"Blog-{blog.id}",
        mapping = {
            "id": blog.id,
            "title": blog.title,
            "slug": blog.slug,
            "content": blog.content,
            "author_id": blog.author_id,
            "created_at": str(blog.created_at),
            "is_active": str(blog.is_active)
        },
    )
    return blog

def retrieve_blog(id: int, db: Session):
    if r.exists(f"Blog-{id}"):
        temp_blog = r.hgetall(f"Blog-{id}")
        blog = Blog(
            title = temp_blog["title"],
            slug = temp_blog["slug"],
            content = temp_blog["content"],
            author_id = temp_blog["author_id"],
            created_at = temp_blog["created_at"],
            is_active = temp_blog["is_active"]
        )
        print("Retreived from Redis")
    else:
        blog = db.query(Blog).filter(Blog.id == id).first()
        if blog:
            r.hset(
                f"Blog-{blog.id}",
                mapping = {
                    "id": blog.id,
                    "title": blog.title,
                    "slug": blog.slug,
                    "content": blog.content,
                    "author_id": blog.author_id,
                    "created_at": str(blog.created_at),
                    "is_active": str(blog.is_active)
                },
            )
        print("Retrieved from Postgres")
    return blog

def list_blogs(db: Session):
    blogs_in_redis = r.keys(f"Blog-*")
    blogs = []
    if blogs_in_redis != []:
        for blog in blogs_in_redis:
            temp = r.hgetall(blog)
            if temp["is_active"] == "True":
                blogs.append(temp)
        print("Retreived from Redis")
    else:
        blogs = db.query(Blog).filter(Blog.is_active == True).all()
        print("Retrieved from Postgres")
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
    db.refresh(blog_in_db)
    r.hset(
        f"Blog-{blog_in_db.id}",
        mapping = {
            "id": blog_in_db.id,
            "title": blog_in_db.title,
            "slug": blog_in_db.slug,
            "content": blog_in_db.content,
            "author_id": blog_in_db.author_id,
            "created_at": str(blog_in_db.created_at),
            "is_active": str(blog_in_db.is_active)
        },
    )
    return blog_in_db

def delete_blog_by_id(id: int, db: Session, author_id: int):
    blog_in_db = db.query(Blog).filter(Blog.id == id)
    if not blog_in_db.first():
        return {"error": f"Could not find blog with id {id}"}
    if not blog_in_db.first().author_id == author_id:
        return {"error": "Only the author can delete the blog"}
    blog_in_db.delete()
    db.commit()
    if r.exists(f"Blog-{id}"):
        r.delete(f"Blog-{id}")
    return {"msg": f"Deleted blog with id {id}"}