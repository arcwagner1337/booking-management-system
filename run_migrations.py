#!/usr/bin/env python
"""Run Alembic migrations with environment variables from .env"""

import os
from pathlib import Path

from alembic.config import Config
from dotenv import load_dotenv

# Load .env file
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    load_dotenv(env_file)

# Setup Alembic configuration
alembic_cfg = Config("alembic.ini")
alembic_cfg.set_main_option(
    "sqlalchemy.url",
    (
        f"postgresql+asyncpg://"
        f"{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:"
        f"{os.getenv('POSTGRES_PORT')}/"
        f"{os.getenv('POSTGRES_DB')}"
    ),
)
