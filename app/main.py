from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from db.database import Base, engine 
from routers import users, projects, categories


def create_tables():         
	Base.metadata.create_all(bind=engine)
     
def set_cors_headers(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.CORS_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
    app = set_cors_headers(app=app)
    create_tables()
    return app


app = start_application()
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(categories.router)


@app.get("/")
async def root():
    return {"message": "API root endpoint, API is working..."}