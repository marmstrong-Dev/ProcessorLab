import unittest
from src.data.account import Account
from src.datacon import DataCon
from bcrypt import hashpw, gensalt
from app import app
from flask import json
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta


class AuthTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        mdb = DataCon.get_instance()
        db = mdb.get_db()

        self.account = Account(
            "Test", "User", "test_user@address.com",
            hashpw("Password123".encode("utf-8"), gensalt()), True)
        db.accounts.insert_one(self.account.__dict__())

        self.login_data = {
            "email_address": "test_user@address.com", "password": "Password123"}

        self.update_data = {
            "first_name": "Test", "last_name": "User",
            "email_address": "test_user@address.com", "password": "Password123"}

        self.deactivate_data = {
            "email_address": "test_user@address.com"}

        self.register_data = {
            "first_name": "Test", "last_name": "User",
            "email_address": "test_user2@address.com", "password": "Password1234"}

    def test_register(self):
        response = self.app.post(
            "/api/auth/register", data=json.dumps(self.register_data),
            content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Account created successfully")

    def test_login(self):
        response = self.app.post(
            "/api/auth/login", data=json.dumps(self.login_data),
            content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.json.keys(), ["access_token", "refresh_token"])

    def test_refresh(self):
        response = self.app.post(
            "/api/auth/login", data=json.dumps(self.login_data),
            content_type="application/json")

        refresh_token = response.json['refresh_token']

        response = self.app.post(
            "/api/auth/refresh", data=json.dumps({"refresh_token": refresh_token}),
            headers={"Authorization": f"Bearer {refresh_token}"},
            content_type="application/json")

        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.json.keys(), ["access_token", "refresh_token"])

    def test_deactivate(self):
        response = self.app.post(
            "/api/auth/login", data=json.dumps(self.login_data),
            content_type="application/json")

        access_token = response.json['access_token']

        response = self.app.post(
            "/api/auth/status", data=json.dumps(self.deactivate_data),
            content_type="application/json", headers={"Authorization": f"Bearer {access_token}"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Account deactivated successfully")

    def test_update(self):
        response = self.app.post(
            "/api/auth/login", data=json.dumps(self.login_data),
            content_type="application/json")

        access_token = response.json['access_token']

        response = self.app.post(
            "/api/auth/update", data=json.dumps(self.update_data),
            content_type="application/json", headers={"Authorization": f"Bearer {access_token}"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Account updated successfully")

    def tearDown(self):
        mdb = DataCon.get_instance()
        db = mdb.get_db()

        db.accounts.delete_one({"email_address": "test_user@address.com"})
        db.accounts.delete_one({"email_address": "test_user2@address.com"})
