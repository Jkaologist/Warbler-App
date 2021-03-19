"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.testuser1 = User.signup(username="testuser1",
                                email="test1@test.com",
                                password="password1",
                                image_url=None)
        self.testuser2 = User.signup(username="testuser2",
                                email="test2@test.com",
                                password="password2",
                                image_url=None)

        # db.session.add(testuser1, testuser2)
        db.session.commit()

        # self.testuser1 = User.query.all()[0]
        # self.testuser2 = User.query.all()[1]

        self.client = app.test_client()

    def tearDown(self):
        # res = super().tearDown()
        db.session.rollback()
        # return res

    def test_landing_page_route(self):
        with self.client as client:
            rsp = client.get("/")
            html = rsp.get_data(as_text=True)
            self.assertEqual(rsp.status_code, 200)
            self.assertIn("""<div class="home-hero">""", html)

    def test_signup_page_render(self):
        with self.client as client:
            rsp = client.get("/signup")
            html = rsp.get_data(as_text=True)
            self.assertEqual(rsp.status_code, 200)
            self.assertIn("""<h2 class="join-message">Join Warbler today.</h2>""", html)

    def test_signup_page_success(self):
        with app.test_client() as client:
            rsp = client.post("/signup", data={"username": "testuser3",
                                               "email": "test3@test.com",
                                               "password": "password3",
                                               "image_url": None})

            self.assertEqual(len(User.query.all()), 3)
            self.assertEqual(rsp.status_code, 302)

    def test_signup_page_user_dupe(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                self.assertEqual(sess.get(CURR_USER_KEY), None)
            rsp = client.post("/signup", data={"username": "testuser1",
                                                "email": "sup@gmail.com",
                                                "password": "password3",
                                                "image_url": None})
            
            html = rsp.get_data(as_text=True)
            self.assertEqual(rsp.status_code, 200)
            self.assertIn("Username already taken", html)
    

    def test_loads_followers(self):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id
            rsp = client.get(f"/users/{sess[CURR_USER_KEY]}/followers")

            html = rsp.get_data(as_text=True)
            self.assertEqual(rsp.status_code, 200)
            self.assertIn('this is followers.html', html)
    
    def test_loads_followers_logged_out(self):
        with app.test_client() as client:
            rsp = client.get(f"/users/{self.testuser2.id}/followers", follow_redirects=True)
        
            html = rsp.get_data(as_text=True)
            self.assertEqual(rsp.status_code, 200)
            self.assertIn('Access unauthorized.', html)

    # edit
    # following page
    # likes


