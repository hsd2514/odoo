# config.py: Environment variables & settings
import os
from dotenv import load_dotenv

load_dotenv()

# Example for PostgreSQL:
# DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5432/skillswap"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:0314@localhost:5432/skillswap")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
