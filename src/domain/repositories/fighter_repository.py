"""FighterRepository — domain operations for the Fighter aggregate root."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.models.fighter import Fighter
from src.domain.models.medical_record import MedicalRecord
from src.domain.models.fighter_category_registration import FighterCategoryRegistration
from .base_repository import BaseRepository


class FighterRepository(BaseRepository[Fighter]):
    """
    Repository for the Fighter aggregate root.

    In addition to standard CRUD, exposes:
      - get_by_last_name()
      - get_by_belt_level()
      - get_by_country()
      - get_paginated()
      - add_medical_record()
      - approve_registration()
    """

    def __init__(self, session: Session) -> None:
        super().__init__(session, Fighter)

    # ── Specific queries ───────────────────────────────────────────────────────

    def get_by_last_name(self, last_name: str) -> List[Fighter]:
        """Return all fighters whose last name matches (case-insensitive)."""
        stmt = select(Fighter).where(
            Fighter.last_name.ilike(f"%{last_name}%")
        )
        return list(self._session.scalars(stmt).all())

    def get_by_belt_level(self, belt_level: str) -> List[Fighter]:
        """Return all fighters with a given belt level."""
        stmt = select(Fighter).where(Fighter.belt_level == belt_level)
        return list(self._session.scalars(stmt).all())

    def get_by_country(self, country: str) -> List[Fighter]:
        """Return all fighters from a given country."""
        stmt = select(Fighter).where(Fighter.country == country)
        return list(self._session.scalars(stmt).all())

    def get_by_email(self, email: str) -> Optional[Fighter]:
        """Return a fighter by their email address (unique)."""
        stmt = select(Fighter).where(Fighter.email == email)
        return self._session.scalars(stmt).first()

    # ── Pagination (Fighter has the highest expected row count) ───────────────

    def get_paginated(self, page: int = 1, page_size: int = 10) -> List[Fighter]:
        """
        Return a page of fighters ordered by last_name, first_name.

        Args:
            page:      1-based page index.
            page_size: Number of records per page.

        Returns:
            A list of Fighter instances for the requested page.
        """
        offset = (page - 1) * page_size
        stmt = (
            select(Fighter)
            .order_by(Fighter.last_name, Fighter.first_name)
            .limit(page_size)
            .offset(offset)
        )
        return list(self._session.scalars(stmt).all())

    def count(self) -> int:
        """Return the total number of fighters in the database."""
        from sqlalchemy import func, select

        stmt = select(func.count()).select_from(Fighter)
        return self._session.execute(stmt).scalar_one()

    # ── Domain operations ─────────────────────────────────────────────────────

    def add_medical_record(
        self,
        fighter_id: int,
        blood_type: Optional[str] = None,
        notes: Optional[str] = None,
        conditions: Optional[str] = None,
        doctor_name: Optional[str] = None,
    ) -> MedicalRecord:
        """
        Create and attach a MedicalRecord to an existing Fighter.

        Raises ValueError if the fighter does not exist or already has a record.
        """
        fighter = self.get(fighter_id)
        if fighter is None:
            raise ValueError(f"Fighter with id={fighter_id} not found.")
        if fighter.medical_record is not None:
            raise ValueError(
                f"Fighter id={fighter_id} already has a medical record."
            )
        record = MedicalRecord(
            fighter_id=fighter_id,
            blood_type=blood_type,
            notes=notes,
            conditions=conditions,
            doctor_name=doctor_name,
        )
        self._session.add(record)
        self._session.flush()
        return record

    def approve_registration(
        self,
        fighter_id: int,
        category_id: int,
        tournament_id: int,
    ) -> FighterCategoryRegistration:
        """
        Mark a fighter's category registration as approved.

        Raises ValueError if the registration does not exist.
        """
        stmt = select(FighterCategoryRegistration).where(
            FighterCategoryRegistration.fighter_id == fighter_id,
            FighterCategoryRegistration.category_id == category_id,
            FighterCategoryRegistration.tournament_id == tournament_id,
        )
        reg = self._session.scalars(stmt).first()
        if reg is None:
            raise ValueError(
                f"Registration not found for fighter={fighter_id}, "
                f"category={category_id}, tournament={tournament_id}."
            )
        reg.is_approved = True
        self._session.flush()
        return reg
