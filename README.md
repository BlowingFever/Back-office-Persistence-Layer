# Gestor de Torneos de Deportes de Contacto
## Persistence Layer — SQLAlchemy ORM + Alembic

---

## Project structure

```
Back-office-Persistence-Layer/
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 001_initial_schema.py  
│       └── 002_add_last_update.py    
├── alembic.ini
├── config/
│   ├── __init__.py
│   └── database.py                 
├── notebooks/
│   └── test_repositories.ipynb      
├── requirements.txt
├── docker-compose.yml             
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
└── .env                           
```

---

## Requirements

- Python 3.11+
- Docker Desktop (running)
- Git

---

## First-time setup

### 1. Clone the repository

```bash
git clone https://github.com/BlowingFever/Back-office-Persistence-Layer.git
cd Back-office-Persistence-Layer
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Mac / Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your database credentials:

```env
APP_ENV=development

DATABASE_URL_TEST=sqlite:///./test_tournament.db
DATABASE_URL_DEVELOPMENT=postgresql+psycopg2://tournament_user:tournament_pass@localhost:5432/tournament_dev
DATABASE_URL_PRODUCTION=postgresql+psycopg2://tournament_user:tournament_pass@localhost:5432/tournament_prod
```

| `APP_ENV`     | Database used                           |
|---------------|-----------------------------------------|
| `test`        | SQLite (`DATABASE_URL_TEST`)            |
| `development` | PostgreSQL (`DATABASE_URL_DEVELOPMENT`) |
| `production`  | PostgreSQL (`DATABASE_URL_PRODUCTION`)  |

### 5. Start PostgreSQL with Docker

Make sure Docker Desktop is open, then run:

```bash
docker compose up -d
```

Verify the container is running:

```bash
docker compose ps
# Expected: tournament_db   Up   0.0.0.0:5432->5432/tcp
```

### 6. Run database migrations

```bash
alembic upgrade head
```

Expected output:
```
Running upgrade  -> 001_initial_schema, Initial schema creation
Running upgrade 001_initial_schema -> 002_add_last_update, Added last_update attribute
```

### 7. Verify the setup

```bash
python verify.py
```

Expected output:
```
🏆  All checks passed — project is correctly structured.
```

---

## Daily workflow

### Start the database

```bash
# Make sure Docker Desktop is open, then:
docker compose up -d
source .venv/bin/activate
```

### Stop the database

```bash
docker compose down
```

### Run the notebook tests

```bash
jupyter notebook notebooks/test_repositories.ipynb
```

Run all cells top to bottom. All assertions must pass.

---

## Alembic migrations reference

```bash
# Apply all pending migrations
alembic upgrade head

# Check current revision
alembic current

# Show full history
alembic history

# Downgrade one step
alembic downgrade -1

# Downgrade to beginning (wipes schema)
alembic downgrade base
```

---

## Docker reference

```bash
# Start Postgres in background
docker compose up -d

# Stop Postgres
docker compose down

# Stop and delete all data (full reset)
docker compose down -v

# View Postgres logs
docker compose logs db

# Connect directly to the database
docker exec -it tournament_db psql -U tournament_user -d tournament_dev
```

---

## Domain model summary

| Table                           | Type              | Description                              |
|---------------------------------|-------------------|------------------------------------------|
| `fighter`                       | Aggregate root    | Competition participant                  |
| `medical_record`                | 1:1 → fighter     | Medical information per fighter          |
| `tournament`                    | Aggregate root    | Competition event                        |
| `tatami`                        | 1:N → tournament  | Competition mat                          |
| `category`                      | Aggregate root    | Division (belt + weight + gender)        |
| `fighter_category_registration` | N:M with attrs    | Fighter enrolled in category/tournament  |
| `match`                         | 1:N → tournament  | Single bout between two fighters         |

---

## Repository methods

### FighterRepository

| Method                      | Description                            |
|-----------------------------|----------------------------------------|
| `add(fighter)`              | Persist new fighter                    |
| `get(id)`                   | Find by PK                             |
| `get_all()`                 | All fighters                           |
| `update(fighter)`           | Save changes                           |
| `delete(fighter)`           | Remove fighter                         |
| `get_by_last_name(name)`    | Filter by last name                    |
| `get_by_belt_level(level)`  | Filter by belt                         |
| `get_by_country(country)`   | Filter by country                      |
| `get_by_email(email)`       | Find by email                          |
| `get_paginated(page, size)` | Paginated list                         |
| `count()`                   | Total number of fighters               |
| `add_medical_record(...)`   | Domain op: attach medical record       |
| `approve_registration(...)` | Domain op: approve a registration      |

### TournamentRepository

| Method                          | Description                  |
|---------------------------------|------------------------------|
| `add / get / get_all / update / delete` | CRUD                 |
| `get_by_name(name)`             | Filter by name               |
| `get_by_location(location)`     | Filter by location           |
| `get_active_tournaments()`      | Future/ongoing events        |
| `get_upcoming()`                | Not yet started              |
| `add_tatami_to_tournament(...)` | Domain op: create tatami     |

### CategoryRepository

| Method                          | Description                  |
|---------------------------------|------------------------------|
| `add / get / get_all / update / delete` | CRUD                 |
| `get_by_name(name)`             | Filter by name               |
| `get_by_belt_level(level)`      | Filter by belt               |
| `get_by_gender(gender)`         | Filter by gender             |
| `get_by_weight_range(min, max)` | Filter by weight range       |

### MatchRepository

| Method                              | Description                     |
|-------------------------------------|---------------------------------|
| `add / get / get_all / update / delete` | CRUD                        |
| `get_by_tournament(id)`             | Matches in a tournament         |
| `get_by_fighter(id)`                | All matches for a fighter       |
| `get_by_category(id)`               | Matches in a category           |
| `get_by_round(tournament_id, round)`| Matches in a specific round     |
| `get_wins_by_fighter(id)`           | Matches won by a fighter        |

### RegistrationRepository

| Method                          | Description                              |
|---------------------------------|------------------------------------------|
| `add / get / get_all / update / delete` | CRUD                             |
| `get(tuple)`                    | Find by composite PK `(fighter_id, category_id, tournament_id)` |
| `get_by_tournament(id)`         | Registrations for a tournament           |
| `get_by_fighter(id)`            | Registrations for a fighter              |
| `get_pending_approvals(id)`     | Unapproved registrations                 |

---

## Troubleshooting

**`ImportError: cannot import name 'Base'`**
The `src/domain/models/__init__.py` is empty. Add the imports listed in the setup guide.

**`connection refused` on port 5432**
Docker Desktop is not running or the container is stopped. Run `docker compose up -d`.

**`alembic: command not found`**
The virtual environment is not active. Run `source .venv/bin/activate`.

**`ModuleNotFoundError: No module named 'src'`**
Run all commands from the project root directory, not from inside a subfolder.