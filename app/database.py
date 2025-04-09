from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL from environment or use default SQLite location
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wayv_integration.db")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Function to create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Session dependency for endpoints
def get_session():
    with Session(engine) as session:
        yield session
