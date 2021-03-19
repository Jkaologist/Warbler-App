"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class MessageModelTestCase(TestCase):
    """Test model for messages"""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        msg = Message(
            text="yoyo",
            timestamp=datetime.utcnow()
        )

        db.session.commit()

        self.msg = msg
    
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_test_model(self):
        """ Tests if message test works """

        self.assertEqual(self.msg.text, "yoyo")
    
    def test_message_timestamp(self):
        """ Tests if datetime is returned """

        self.assertIsInstance(self.msg.timestamp, datetime)
    
    

        