# Gestor de Torneos de Deportes de Contacto
## Persistence Layer — SQLAlchemy ORM + Alembic

---

## Project structure

```
tournament_manager/
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 001_initial_schema.py     ← Migration 1: full schema
│       └── 002_add_last_update.py    ← Migration 2: last_update column
├── alembic.ini
├── config/
│   ├── __init__.py
│   └── database.py                   ← env-based DB URL selector
├── notebooks/
│   └── test_repositories.ipynb       ← All repository tests
├── requirements.txt
├── src/
│   └── domain/
│       ├── models/
│       │   ├── base.py
│       │   ├── fighter.py
│       │   ├── medical_record.py
│       │   ├── tournament.py
│       │   ├── tatami.py
│       │   ├── category.py
│       │   ├── fighter_category_registration.py
│       │   └── match.py
│       └── repositories/
│           ├── base_repository.py
│           ├── fighter_repository.py
│           ├── tournament_repository.py
│           ├── category_repository.py
│           ├── match_repository.py
│           ├── registration_repository.py
│           └── unit_of_work.py
├── .env.example
└── .env                              ← copy of .env.example, fill before use
```

---

## Quick start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.example` to `.env` and fill in your database URLs.

| `APP_ENV`    | Database used                          |
|-------------|----------------------------------------|
| `test`      | SQLite (`DATABASE_URL_TEST`)           |
| `development` | PostgreSQL (`DATABASE_URL_DEVELOPMENT`) |
| `production`  | PostgreSQL (`DATABASE_URL_PRODUCTION`)  |

### 3. Run migrations

```bash
# First time — bring schema to latest version
alembic upgrade head

# Check current revision
alembic current

# Show history
alembic history

# Downgrade one step
alembic downgrade -1
```

### 4. Run the notebook tests

```bash
jupyter notebook notebooks/test_repositories.ipynb
```

Run all cells from top to bottom. All assertions must pass.

---

## Domain model summary

| Table                        | Type          | Description                               |
|------------------------------|---------------|-------------------------------------------|
| `fighter`                    | Aggregate root | Competition participant                  |
| `medical_record`             | 1:1 → fighter | Medical information per fighter           |
| `tournament`                 | Aggregate root | Competition event                         |
| `tatami`                     | 1:N → tournament | Competition mat                        |
| `category`                   | Aggregate root | Division (belt + weight + gender)         |
| `fighter_category_registration` | N:M with attrs | Fighter enrolled in category/tournament |
| `match`                      | 1:N → tournament | Single bout between two fighters        |

---

## Repository methods

### FighterRepository
| Method | Description |
|--------|-------------|
| `add(fighter)` | Persist new fighter |
| `get(id)` | Find by PK |
| `get_all()` | All fighters |
| `update(fighter)` | Save changes |
| `delete(fighter)` | Remove fighter |
| `get_by_last_name(name)` | Filter by last name |
| `get_by_belt_level(level)` | Filter by belt |
| `get_by_country(country)` | Filter by country |
| `get_by_email(email)` | Find by email |
| `get_paginated(page, page_size)` | Paginated list |
| `count()` | Total number of fighters |
| `add_medical_record(...)` | Domain op: attach medical record |
| `approve_registration(...)` | Domain op: approve a registration |

### TournamentRepository
| Method | Description |
|--------|-------------|
| `add / get / get_all / update / delete` | CRUD |
| `get_by_name(name)` | Filter by name |
| `get_by_location(location)` | Filter by location |
| `get_active_tournaments()` | Future/ongoing events |
| `get_upcoming()` | Not yet started |
| `add_tatami_to_tournament(...)` | Domain op: create tatami |

### CategoryRepository
| Method | Description |
|--------|-------------|
| `add / get / get_all / update / delete` | CRUD |
| `get_by_name(name)` | Filter by name |
| `get_by_belt_level(level)` | Filter by belt |
| `get_by_gender(gender)` | Filter by gender |
| `get_by_weight_range(min, max)` | Filter by weight range |

### MatchRepository
| Method | Description |
|--------|-------------|
| `add / get / get_all / update / delete` | CRUD |
| `get_by_tournament(id)` | Matches in a tournament |
| `get_by_fighter(id)` | All matches for a fighter |
| `get_by_category(id)` | Matches in a category |
| `get_by_round(tournament_id, round)` | Matches in a specific round |
| `get_wins_by_fighter(id)` | Matches won by a fighter |

### RegistrationRepository
| Method | Description |
|--------|-------------|
| `add / get / get_all / update / delete` | CRUD |
| `get(tuple)` | Find by composite PK `(fighter_id, category_id, tournament_id)` |
| `get_by_tournament(id)` | Registrations for a tournament |
| `get_by_fighter(id)` | Registrations for a fighter |
| `get_pending_approvals(tournament_id)` | Unapproved registrations |
