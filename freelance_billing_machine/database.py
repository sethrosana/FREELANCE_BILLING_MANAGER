from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///freelance_billing.db"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# ✅ Create a global session factory
Session = sessionmaker(bind=engine)

# Declare base for ORM models
Base = declarative_base()


def init_db():
    """Initialize the database tables."""
    from .models import Client, Project, Invoice, WorkLog
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")

