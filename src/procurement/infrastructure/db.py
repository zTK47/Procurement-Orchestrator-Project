"""SQLAlchemy engine and session setup.

Status: scaffolded, NOT YET wired into main.py. The current prototype
(Phase 3 - Develop) runs on the in-memory repositories so that the domain
and application logic can be fully TDD'd without requiring a running
database. Swapping to Postgres-backed repositories is tracked as the
Phase 4 (Validate) milestone in docs/TASKS.md.

Expected environment variable:
    DATABASE_URL  e.g. postgresql+psycopg2://user:password@host/dbname
    (see Neon.tech connection string format)
"""
from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/procurement"
)


def get_engine():
    return create_engine(DATABASE_URL, pool_pre_ping=True)


def get_session_factory():
    return sessionmaker(bind=get_engine(), autocommit=False, autoflush=False)
