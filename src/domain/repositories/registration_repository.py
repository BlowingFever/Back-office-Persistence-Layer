"""RegistrationRepository — CRUD for FighterCategoryRegistration."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.models.fighter_category_registration import FighterCategoryRegistration
from .base_repository import BaseRepository


class RegistrationRepository(BaseRepository[FighterCategoryRegistration]):
    """
    Repository for FighterCategoryRegistration (N:M with attributes).

    The composite PK is (fighter_id, category_id, tournament_id), so
    get() uses a tuple rather than a single integer.
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session, FighterCategoryRegistration)

    # Override get to handle composite PK
    def get(self, pk) -> Optional[FighterCategoryRegistration]:  # type: ignore[override]
        """
        Retrieve by composite PK.

        Args:
            pk: A tuple (fighter_id, category_id, tournament_id).
        """
        fighter_id, category_id, tournament_id = pk
        stmt = select(FighterCategoryRegistration).where(
            FighterCategoryRegistration.fighter_id == fighter_id,
            FighterCategoryRegistration.category_id == category_id,
            FighterCategoryRegistration.tournament_id == tournament_id,
        )
        return self._session.scalars(stmt).first()

    def get_by_tournament(self, tournament_id: int) -> List[FighterCategoryRegistration]:
        """Return all registrations for a tournament."""
        stmt = select(FighterCategoryRegistration).where(
            FighterCategoryRegistration.tournament_id == tournament_id
        )
        return list(self._session.scalars(stmt).all())

    def get_by_fighter(self, fighter_id: int) -> List[FighterCategoryRegistration]:
        """Return all registrations for a fighter."""
        stmt = select(FighterCategoryRegistration).where(
            FighterCategoryRegistration.fighter_id == fighter_id
        )
        return list(self._session.scalars(stmt).all())

    def get_pending_approvals(self, tournament_id: int) -> List[FighterCategoryRegistration]:
        """Return unapproved registrations for a tournament."""
        stmt = select(FighterCategoryRegistration).where(
            FighterCategoryRegistration.tournament_id == tournament_id,
            FighterCategoryRegistration.is_approved == False,  # noqa: E712
        )
        return list(self._session.scalars(stmt).all())
