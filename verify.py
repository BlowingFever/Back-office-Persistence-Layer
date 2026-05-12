"""
verify.py — Quick sanity-check: imports all modules and verifies the schema
can be created in an in-memory SQLite database.

Usage:
    python verify.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

os.environ["APP_ENV"] = "test"
os.environ["DATABASE_URL_TEST"] = "sqlite:///:memory:"

print("Checking imports...")

# Models
from src.domain.models import (  # noqa: F401
    Base, Fighter, MedicalRecord, Tournament, Tatami,
    Category, FighterCategoryRegistration, Match,
)
print("  ✅  All ORM models imported")

# Repositories
from src.domain.repositories import (  # noqa: F401
    FighterRepository, TournamentRepository, CategoryRepository,
    MatchRepository, RegistrationRepository, UnitOfWork,
)
print("  ✅  All repositories imported")

# Config
from config.database import get_engine, get_session_factory  # noqa: F401
print("  ✅  Config module imported")

# Schema creation
from sqlalchemy import create_engine, inspect

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)

insp = inspect(engine)
tables = insp.get_table_names()
expected = {
    "fighter", "medical_record", "tournament", "tatami",
    "category", "fighter_category_registration", "match",
}
missing = expected - set(tables)
assert not missing, f"Missing tables: {missing}"
print(f"  ✅  Schema created — {len(tables)} tables: {sorted(tables)}")

# Verify last_update column is defined on models (it's in Migration 2 but
# the ORM column is always declared; it will be added via Alembic)
from sqlalchemy import inspect as sa_inspect

for cls in [Fighter, MedicalRecord, Tournament, Tatami, Category,
            FighterCategoryRegistration, Match]:
    mapper = sa_inspect(cls)
    col_names = [c.key for c in mapper.columns]
    assert "last_update" in col_names, f"last_update missing in {cls.__name__}"

print("  ✅  last_update column declared on all ORM models")

print("\n🏆  All checks passed — project is correctly structured.")