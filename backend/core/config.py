# Database URL
# SQLALCHEMY_DATABASE_URL = 'sqlite:///backend/database/database.db'
SQLALCHEMY_DATABASE_URL = 'postgresql://jhtw6nsf:475fa74c47d1@localhost:5432/db'

# JWT
SECRET_KEY = '552bf2aa0ce05502ad1a291ab9661dd8201fcd0b197de1dabfa0a338f9b2ccf3'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Train game endpoint
TRAIN_GAME_URL = 'http://localhost:8002/api/v1/train/'
