"""
Usage:
    python seed.py                  # uses APP_ENV from .env
    APP_ENV=test python seed.py
"""

import os
import sys
from datetime import datetime, timedelta

# Make project root importable
sys.path.insert(0, os.path.dirname(__file__))

from config.database import get_engine, get_session_factory
from src.domain.models import Base, Fighter, Tournament, Category
from src.domain.models import FighterCategoryRegistration, Match, Tatami
from src.domain.repositories import UnitOfWork


def seed():
    engine = get_engine(echo=False)
    Base.metadata.create_all(engine)  # ensure tables exist
    Session = get_session_factory(engine)

    with UnitOfWork(session_factory=Session) as uow:
        # ── Fighters ──────────────────────────────────────────────────────────
        fighters = [
            Fighter(first_name="Ana",     last_name="García",   gender="F",
                    belt_level="blue",   club_name="Club BCN",  country="Spain",
                    email="ana@example.com"),
            Fighter(first_name="Carlos",  last_name="López",    gender="M",
                    belt_level="black",  club_name="Dojo MAD",  country="Spain",
                    email="carlos@example.com"),
            Fighter(first_name="Yuki",    last_name="Tanaka",   gender="F",
                    belt_level="purple", club_name="Osaka Dojo",country="Japan",
                    email="yuki@example.com"),
            Fighter(first_name="Mohamed", last_name="Ali",      gender="M",
                    belt_level="brown",  club_name="Cairo FC",  country="Egypt",
                    email="mohamed@example.com"),
            Fighter(first_name="Laura",   last_name="Smith",    gender="F",
                    belt_level="blue",   club_name="London Judo",country="UK",
                    email="laura@example.com"),
        ]
        for f in fighters:
            uow.fighters.add(f)
        uow.commit()
        print(f"✅  {len(fighters)} fighters inserted")

        # ── Categories ────────────────────────────────────────────────────────
        categories = [
            Category(name="Blue -57 kg M",  belt_level="blue",   weight_min_kg=0,  weight_max_kg=57,  gender="M"),
            Category(name="Blue -70 kg F",  belt_level="blue",   weight_min_kg=57, weight_max_kg=70,  gender="F"),
            Category(name="Black -70 kg M", belt_level="black",  weight_min_kg=0,  weight_max_kg=70,  gender="M"),
            Category(name="Purple -57 kg F",belt_level="purple", weight_min_kg=0,  weight_max_kg=57,  gender="F"),
        ]
        for c in categories:
            uow.categories.add(c)
        uow.commit()
        print(f"✅  {len(categories)} categories inserted")

        # ── Tournaments ───────────────────────────────────────────────────────
        now = datetime.utcnow()
        t1 = Tournament(
            name="Copa Primavera 2026",
            location="Barcelona",
            start_date=now + timedelta(days=30),
            end_date=now + timedelta(days=31),
            max_fighters=64,
        )
        t2 = Tournament(
            name="Grand Prix Madrid 2026",
            location="Madrid",
            start_date=now + timedelta(days=90),
            end_date=now + timedelta(days=92),
            max_fighters=128,
        )
        uow.tournaments.add(t1)
        uow.tournaments.add(t2)
        uow.commit()
        print(f"✅  2 tournaments inserted: '{t1.name}', '{t2.name}'")

        # ── Tatamis ───────────────────────────────────────────────────────────
        uow.tournaments.add_tatami_to_tournament(
            t1.tournament_id, name="Tatami A", mat_number=1, area_size=64.0)
        uow.tournaments.add_tatami_to_tournament(
            t1.tournament_id, name="Tatami B", mat_number=2, area_size=64.0)
        uow.commit()
        print("✅  2 tatamis inserted for Copa Primavera")

        # ── Medical records ───────────────────────────────────────────────────
        uow.fighters.add_medical_record(
            fighters[0].fighter_id,
            blood_type="A+", notes="No known conditions", doctor_name="Dr. Pérez")
        uow.fighters.add_medical_record(
            fighters[1].fighter_id,
            blood_type="O-", notes="Mild asthma",         doctor_name="Dr. Ruiz")
        uow.commit()
        print("✅  2 medical records inserted")

        # ── Registrations ─────────────────────────────────────────────────────
        regs = [
            FighterCategoryRegistration(
                fighter_id=fighters[0].fighter_id,
                category_id=categories[1].category_id,
                tournament_id=t1.tournament_id,
                weight_in_weight_kg=56.2, is_approved=True),
            FighterCategoryRegistration(
                fighter_id=fighters[1].fighter_id,
                category_id=categories[2].category_id,
                tournament_id=t1.tournament_id,
                weight_in_weight_kg=68.5, is_approved=True),
            FighterCategoryRegistration(
                fighter_id=fighters[2].fighter_id,
                category_id=categories[3].category_id,
                tournament_id=t1.tournament_id,
                weight_in_weight_kg=55.0, is_approved=False),
            FighterCategoryRegistration(
                fighter_id=fighters[3].fighter_id,
                category_id=categories[0].category_id,
                tournament_id=t1.tournament_id,
                weight_in_weight_kg=56.8, is_approved=True),
        ]
        for r in regs:
            uow.registrations.add(r)
        uow.commit()
        print(f"✅  {len(regs)} registrations inserted")

        # ── Matches ───────────────────────────────────────────────────────────
        matches = [
            Match(
                tournament_id=t1.tournament_id,
                category_id=categories[1].category_id,
                blue_fighter_id=fighters[0].fighter_id,
                red_fighter_id=fighters[2].fighter_id,
                winner_id=fighters[0].fighter_id,
                round_number=1,
                duration_seconds=185.0,
                win_method="ippon",
                scheduled_time=now + timedelta(days=30, hours=9),
            ),
            Match(
                tournament_id=t1.tournament_id,
                category_id=categories[2].category_id,
                blue_fighter_id=fighters[1].fighter_id,
                red_fighter_id=fighters[3].fighter_id,
                winner_id=fighters[1].fighter_id,
                round_number=1,
                duration_seconds=245.0,
                win_method="waza-ari",
                scheduled_time=now + timedelta(days=30, hours=10),
            ),
        ]
        for m in matches:
            uow.matches.add(m)
        uow.commit()
        print(f"✅  {len(matches)} matches inserted")

    print("\n🏆  Seed completed successfully.")


if __name__ == "__main__":
    seed()
