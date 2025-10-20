import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Read the database URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please check your .env file.")

# ✅ Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# ✅ Create a global session factory
Session = sessionmaker(bind=engine)

# ✅ Declare base for ORM models
Base = declarative_base()

def init_db():
    """Initialize the database tables."""
    from .models import Client, Project, Invoice, WorkLog
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")
