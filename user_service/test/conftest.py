import hashlib
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import StaticPool

# Import your real model base & User
from app.models.user_model import Base, User  # Base should be your DeclarativeBase

@pytest.fixture(scope="session")
def engine():
    # In-memory SQLite that persists for the whole test session
    eng = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(eng)
    try:
        yield eng
    finally:
        Base.metadata.drop_all(eng)
        clear_mappers()

@pytest.fixture()
def db(engine):
    # New Session per test, wrapped in a transaction for isolation
    connection = engine.connect()
    trans = connection.begin()
    SessionLocal = sessionmaker(bind=connection, autoflush=False, autocommit=False, future=True)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        trans.rollback()
        connection.close()

@pytest.fixture()
def user_factory(db):
    def _make_user(username: str, password: str):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        u = User(username=username, hashed_password=hashed)
        db.add(u)
        db.commit()
        db.refresh(u)
        return u
    return _make_user
