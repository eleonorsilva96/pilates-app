from dotenv import load_dotenv
import os

load_dotenv()

class DevConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URL")
    SECRET_KEY=os.getenv("JWT_SECRET_KEY")
    # add app-specific constants
    TOTAL_CLASSES = 144
    TOTAL_TEACHERS = 4