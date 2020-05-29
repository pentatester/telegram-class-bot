"""Drop and create a new database with schema."""

from sqlalchemy_utils.functions import create_database
from klassbot.db import engine, base
from klassbot.models import *  # noqa

db_url = engine.url
create_database(db_url)
# with engine.connect() as con:
#     con.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
base.metadata.create_all()
