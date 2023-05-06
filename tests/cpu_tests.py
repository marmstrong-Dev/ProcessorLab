import unittest
from bcrypt import hashpw, gensalt
from flask import json
from src.data.central_processor import CentralProcessor
from src.data.account import Account
from src import db
from app import app


class TestCpu(unittest.TestCase):
    def setUp(self):
        self.test_cpu = CentralProcessor(
            "Test - Intel", "Core i9-13900KF", "LGA1700",
            16, 24, 5.4, True)

        self.test_cpus = [
            CentralProcessor(
                "Test - AMD", "Ryzen 7 7800X3D", "AM5",
                8, 16, 5.0, False),
            CentralProcessor(
                "Test - Intel", "Core i7-13700K", "LGA1700",
                16, 24, 5.4, True),
            CentralProcessor(
                "Test - AMD", "Ryzen 9 7900X", "AM5",
                12, 24, 5.6, False)
        ]

        self.app = app.test_client()
        self.test_cpu_id = None

        self.test_user = Account(
            "Test", "User", "test_user@address.com",
            hashpw("Password123".encode("utf-8"), gensalt()), True)

        db.accounts.insert_one(self.test_user.__dict__())

        self.login_data = {"email_address": "test_user@address.com", "password": "Password123"}

        # Generate access token
        response = self.app.post(
            "/api/auth/login", data=json.dumps(self.login_data),
            content_type="application/json")

        self.access_token = response.json['access_token']

    def test_get_cpu_by_query(self):
        response = self.app.get(
            "/api/cpu/filtered/params$brand=Test%20-%20Intel$model=Core%20i9-13900KF$socket=LGA1700",
            headers={"Authorization": f"Bearer {self.access_token}"})

        self.assertEqual(response.status_code, 200)

    def test_add_cpu(self):
        response = self.app.post(
            "/api/cpu/add", data=json.dumps(self.test_cpu.__json__()),
            headers={"Authorization": f"Bearer {self.access_token}"},
            content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.test_cpu_id = response.json['data']['_id']

    def test_add_multiple_cpus(self):
        response = self.app.post(
            "/api/cpu/add/batch", data=json.dumps([cpu.__json__() for cpu in self.test_cpus]),
            headers={"Authorization": f"Bearer {self.access_token}"},
            content_type="application/json")

        self.assertEqual(response.status_code, 200)

    def test_get_cpu(self):
        self.test_add_cpu()
        url_id = self.test_cpu_id

        response = self.app.get(
            f"/api/cpu/{url_id}", headers={"Authorization": f"Bearer {self.access_token}"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['data']['_id'], self.test_cpu_id)

    def test_get_all_cpus(self):
        response = self.app.get("/api/cpu/all", headers={"Authorization": f"Bearer {self.access_token}"})

        self.assertEqual(response.status_code, 200)

    def test_update_cpu(self):
        self.test_add_cpu()
        url_id = self.test_cpu_id

        mod_cpu_data = {
            "brand": "Test - AMD", "model": "Ryzen 7 7800X3D", "socket": "AM5",
            "core_count": 8, "thread_count": 16, "base_clock": 5.0, "unlocked": True
        }

        response = self.app.put(
            f"/api/cpu/update/{url_id}", data=json.dumps(mod_cpu_data),
            headers={"Authorization": f"Bearer {self.access_token}"},
            content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['data']['brand'], "Test - AMD")

    def test_delete_cpu(self):
        self.test_add_cpu()
        url_id = self.test_cpu_id

        response = self.app.delete(
            f"/api/cpu/delete/{url_id}",
            headers={"Authorization": f"Bearer {self.access_token}"})

        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        # Delete test GPUs marked by Test -
        db.cpus.delete_many({"brand": {"$regex": "^Test - "}})
