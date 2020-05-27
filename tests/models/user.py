from .base import BaseTestModel

from datetime import datetime
from sqlalchemy.orm import Session

from klassbot.db import get_session
from klassbot.models import user, User


class TestModule(TestCase):
    MODULES = ["User", "UserKlass", "UserKlassConfig"]

    def test_modules(self):
        for n in self.MODULES:
            self.assertIn(n, user.__all__)

class TestUser(BaseTestModel):
    NAME = "TestName"
    USERNAME = "username"
    STARTED = True
    BANNED = False
    DELETED = False
    BROADCAST_SENT = False
    LAST_UPDATE = datetime.now()
    ADMIN = False
    LOCALE = "English"
    EUROPEAN_DATE_FORMAT = False
    NOTIFICATIONS_ENABLED = True
    EXPECTED_INPUT = ""
    CREATED_AT = 
    UPDATED_AT = 
    USER: User = None

    def setUp(self):
        self.setUpClass()
    
    def tearDown(self):
        self.tearDownClass()
name,
username,
started,
banned,
deleted,
broadcast_sent,
last_update,
admin,
locale,
european_date_format,
notifications_enabled,
expected_input,
created_at,
updated_at,















