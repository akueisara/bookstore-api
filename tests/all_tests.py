import asyncio

from starlette.testclient import TestClient

from models.user import User
from run import app
from utils.db import execute, fetch
from unittest import TestCase

from utils.secuirty import get_hashed_password


class AllTests(TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        self._clear_db()

    def _insert_user(self, username, password):
        query = """insert into users(username, password) values(:username, :password)"""
        hashed_password = get_hashed_password(password)
        values = {"username": username, "password": hashed_password}
        self.loop.run_until_complete(execute(query, False, values))

    def _check_user(self, username, mail):
        query = """select * from personel where username=:username and mail=:mail"""
        values = {"username": username, "mail": mail}

        result = self.loop.run_until_complete(fetch(query, True, values))
        if result:
            return True

        return False

    def _get_auth_header(self):
        self._insert_user("test", "test")
        response = self.client.post("/token", dict(username="test", password="test"))
        jwt = response.json()["access_token"]
        return {"Authorization": f"Bearer {jwt}"}

    def _clear_db(self):
        queries = [
            """delete from users;""",
            """delete from authors;""",
            """delete from books;""",
            """delete from personel;"""
        ]
        for query in queries:
            self.loop.run_until_complete(execute(query, False))

    def test_token_successful(self):
        self._insert_user("user1", "pass1")
        response = self.client.post("/token", dict(username="user1", password="pass1"))

        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_token_unauthorized(self):
        self._insert_user("user1", "pass1")
        response = self.client.post("/token", dict(username="user1", password="wrong_password"))

        assert response.status_code == 401

    def test_post_user(self):
        auth_header = self._get_auth_header()
        user_dict = {"name": "user1", "password": "secret", "mail": "a@b.com", "role": "admin"}

        response = self.client.post("/v1/user", json=user_dict, headers=auth_header)

        assert response.status_code == 201
        assert self._check_user("user1", "a@b.com")

    def test_post_user_wrong_email(self):
        auth_header = self._get_auth_header()
        user_dict = {"name": "user1", "password": "secret", "mail": "invalid", "role": "admin"}

        response = self.client.post("/v1/user", json=user_dict, headers=auth_header)

        assert response.status_code == 422
