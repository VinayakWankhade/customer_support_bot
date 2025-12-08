"""
Global pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

from src.main import app
from src.database import get_db_dependency
from src.models.models import Base

# Use a single test database for all tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_suite.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    """Create engine once per session"""
    return engine

@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Creates a fresh database session for a test.
    Rolls back transaction after test.
    """
    # Create tables
    Base.metadata.create_all(bind=db_engine)
    
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
    # Drop tables to ensure clean state (or just rollback transaction if suitable, 
    # but sqlite DDL might not rollback well, so create/drop is safer for integration)
    Base.metadata.drop_all(bind=db_engine)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Test client with DB dependency override
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db_dependency] = override_get_db
    yield TestClient(app)
    app.dependency_overrides = {}
