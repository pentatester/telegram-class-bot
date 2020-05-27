from unittest import TestCase
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from klassbot.db import get_session


class BaseTestModel(TestCase):
    SESSION: Session = None
    MODEL = None

    @classmethod
    def setUpClass(cls):
        cls.SESSION = get_session()

    @classmethod
    def tearDownClass(cls):
        if isinstance(cls.SESSION, Session):
            Session.close()

    def filter(self, *args, **kwargs):
        try:
            return self.SESSION.query(self.MODEL).filter_by(**kwargs)
        except NoResultFound:
            pass
        return
