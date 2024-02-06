import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from apis_in_ml.main import app, get_db

# Create a database in memory
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# A local session for testing
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the database dependency in the app
def override_get_db():
    SQLModel.metadata.create_all(engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def client() -> TestClient:
    """Test FastAPI client."""
    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)
