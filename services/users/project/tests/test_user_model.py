import unittest
from sqlalchemy.exc import IntegrityError
from flask import current_app
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user()
        self.assertTrue(user.id)
        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.password)
        self.assertTrue(user.active)
        self.assertFalse(user.admin)

    def test_add_user_duplicate_username(self):
        add_user()
        duplicate_user = User(
            username="test",
            email="test@test.com",
            password="test"
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user()
        duplicate_user = User(
            username="justanothertest",
            email="test@test.com",
            password="greaterthaneight"
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user()
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        user_one = add_user()
        user_two = add_user("test2", "test2@test.com", "test")
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token(self):
        user = add_user()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = add_user()
        auth_token = user.encode_auth_token(user.id)
        self.assertEqual(user.decode_auth_token(auth_token), user.id)

    def test_auth_token_incorrect_user_id(self):
        user = add_user()
        auth_token = user.encode_auth_token(user.id + 1)
        self.assertNotEqual(user.decode_auth_token(auth_token), user.id)

    def test_incorrect_auth_token(self):
        user = add_user()
        auth_token = b"testIncorrectAuthToken"
        self.assertEqual(
            user.decode_auth_token(auth_token),
            "Invalid token. Please log in again"
        )

    def test_expired_auth_token(self):
        user = add_user()
        current_app.config["TOKEN_EXPIRATION_SECONDS"] = -1
        auth_token = user.encode_auth_token(user.id)
        self.assertEqual(
            user.decode_auth_token(auth_token),
            "Signature expired. Please log in again"
        )

    def test_two_auth_tokens_for_one_user_match(self):
        user = add_user()
        first_auth_token = user.encode_auth_token(user.id)
        second_auth_token = user.encode_auth_token(user.id)
        self.assertEqual(first_auth_token, second_auth_token)


if __name__ == "__main__":
    unittest.main()
