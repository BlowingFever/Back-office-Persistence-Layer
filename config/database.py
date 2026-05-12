"""
Database configuration module.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

_DATABASE_URLS = {
    "test": os.getenv("DATABASE_URL_TEST", "sqlite:///./test_tournament.db"),
    "development": os.getenv("DATABASE_URL_DEVELOPMENT", ""),
    "production": os.getenv("DATABASE_URL_PRODUCTION", ""),
}


def get_database_url() -> str:
    """Return the database URL for the current environment."""
    env = os.getenv("APP_ENV", "test").lower()
    url = _DATABASE_URLS.get(env)
    if not url:
        raise ValueError(
            f"No DATABASE_URL configured for environment '{env}'. "
            "Check your .env file."
        )
    return url


def get_engine(echo: bool = False):
    """Create and return a SQLAlchemy engine for the current environment."""
    url = get_database_url()
    connect_args = {}
    if url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    return create_engine(url, echo=echo, connect_args=connect_args)


def get_session_factory(engine=None):
    """Return a configured session factory."""
    if engine is None:
        engine = get_engine()
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)
