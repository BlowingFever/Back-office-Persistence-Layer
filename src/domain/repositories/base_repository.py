"""Generic base repository with shared CRUD operations."""

from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from src.domain.models.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """
    Generic repository providing basic CRUD for any ORM model.

    Concrete repositories subclass this and may add domain-specific queries.
    """

    def __init__(self, session: Session, model: Type[T]) -> None:
        self._session = session
        self._model = model

    # ── Create ─────────────────────────────────────────────────────────────────
    def add(self, entity: T) -> T:
        """Persist a new entity (added to the session; commit in UoW)."""
        self._session.add(entity)
        self._session.flush()
        return entity

    # ── Read ───────────────────────────────────────────────────────────────────
    def get(self, pk: int) -> Optional[T]:
        """Retrieve a single entity by its primary-key integer."""
        return self._session.get(self._model, pk)

    def get_all(self) -> List[T]:
        """Retrieve all rows for this model."""
        from sqlalchemy import select

        stmt = select(self._model)
        return list(self._session.scalars(stmt).all())

    # ── Update ─────────────────────────────────────────────────────────────────
    def update(self, entity: T) -> T:
        """Merge an already-tracked or detached entity back into the session."""
        merged = self._session.merge(entity)
        self._session.flush()
        return merged

    # ── Delete ─────────────────────────────────────────────────────────────────
    def delete(self, entity: T) -> None:
        """Remove an entity from the database."""
        self._session.delete(entity)
        self._session.flush()
