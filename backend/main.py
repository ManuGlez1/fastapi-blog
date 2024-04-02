from fastapi import FastAPI
from core.config import settings
from apis.base import api_router
from app.base import app_router
from fastapi.staticfiles import StaticFiles


def include_router(app):
    app.include_router(api_router)
    app.include_router(app_router)

def config_staticfiles(app):
    app.mount("/static", StaticFiles(directory = "static"), name = "static")

def start_application():
    app = FastAPI(title = settings.PROJECT_TITLE, version = settings.PROJECT_VERSION)
    include_router(app)
    config_staticfiles(app)
    return app

app = start_application()
