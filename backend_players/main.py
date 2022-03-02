from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend_players.api.v1 import train, movements, players

app = FastAPI(
    title='Backend Players API',
    description='API definition for the generation of players.'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(train.router)
app.include_router(movements.router)
app.include_router(players.router)
