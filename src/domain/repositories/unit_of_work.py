"""
Unit of Work — manages a single database session shared across all repositories.

Usage:
    with UnitOfWork() as uow:
        fighter = Fighter(first_name="Ana", last_name="Doe", ...)
        uow.fighters.add(fighter)
        uow.commit()
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from config.database import get_session_factory
from .fighter_repository import FighterRepository
from .tournament_repository import TournamentRepository
from .category_repository import CategoryRepository
from .match_repository import MatchRepository
from .registration_repository import RegistrationRepository


class UnitOfWork:
    """
    Context manager that groups all repositories under one SQLAlchemy session.

    - Enter  → creates session + repositories
    - Commit → flushes and commits
    - Exit   → rolls back on exception; closes session always
    """

    def __init__(self, session_factory=None) -> None:
        self._session_factory = session_factory or get_session_factory()

    def __enter__(self) -> "UnitOfWork":
        self._session: Session = self._session_factory()
        self.fighters = FighterRepository(self._session)
        self.tournaments = TournamentRepository(self._session)
        self.categories = CategoryRepository(self._session)
        self.matches = MatchRepository(self._session)
        self.registrations = RegistrationRepository(self._session)
        return self

    def commit(self) -> None:
        """Commit all pending changes to the database."""
        self._session.commit()

    def rollback(self) -> None:
        """Discard all pending changes."""
        self._session.rollback()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.rollback()
        self._session.close()
        return False  # don't suppress exceptions
