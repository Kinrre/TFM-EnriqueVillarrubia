from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.api.dependencies import get_db
from backend.main import app

SQLALCHEMY_DATABASE_URL = 'postgresql://jhtw6nsf:475fa74c47d1@localhost:5432/test'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def login(username: str, password: str):
    response = client.post(
        '/api/v1/auth/token',
        data={'grant_type': 'password', 'username': username, 'password': password}
    )

    token = response.json().get('access_token', '')

    return token
