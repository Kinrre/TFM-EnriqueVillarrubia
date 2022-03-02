from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.api.v1 import auth, games, matches, users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Backend API',
    description='API definition for the backend of users, games and matches.'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth.router)
app.include_router(games.router)
app.include_router(matches.router)
app.include_router(users.router)
