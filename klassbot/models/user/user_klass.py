"""The sqlite model for a user."""
from sqlalchemy import (
    Column,
    ForeignKey,
)
from sqlalchemy.types import (
    BigInteger,
)

from klassbot.db import base


class UserKlassLink(base):
    # user to klass links
    __tablename__ = "user_klass"
    # if klass deleted  -> delete link!
    klass_id = Column(
        BigInteger,
        ForeignKey("klass.id", ondelete="cascade", name="klass"),
        primary_key=True,
    )
    # if user deleted  -> delete link!
    user_id = Column(
        BigInteger,
        ForeignKey("user.id", ondelete="cascade", name="user"),
        primary_key=True,
    )
