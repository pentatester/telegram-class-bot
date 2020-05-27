"""DTO for bot.data"""

from sqlalchemy.orm import Session


class BotData(object):
    def __init__(self, session: Session):
        self._session = Session

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session):
        if not isinstance(session, Session):
            raise ValueError("Not `Session`")
        self._session = session

    @session.deleter
    def session(self):
        if self._session:
            del self._session
