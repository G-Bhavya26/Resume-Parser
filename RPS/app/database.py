import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base

# We will use an environment variable for the Database URL.
# For now, this is a placeholder URL for a local PostgreSQL database.
# Format: postgresql://username:password@server:port/database_name
# Note: The '@' in the password is URL-encoded as '%40'
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Bhavya%40380@localhost:5432/crms_db")

# The engine is the main "Delivery Truck" connection point to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal is our "Factory" that creates new database sessions for every request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session and safely close it after use
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
