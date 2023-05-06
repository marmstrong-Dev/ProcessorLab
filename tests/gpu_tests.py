import unittest
from bcrypt import hashpw, gensalt
from flask import json
from src.data.graphics_processor import GraphicsProcessor
from src.data.account import Account
from src import db
from app import app


class TestGpu(unittest.TestCase):
    def setUp(self):
        self.test_gpu = GraphicsProcessor(
            "Test - MSI", "NVIDIA", "GeForce RTX 4080",
            16, "GDDR6X", 2.61, 3, {"DisplayPort": 3, "HDMI": 1})

        self.test_gpus = [
            GraphicsProcessor(
                "Test - MSI", "AMD", "Radeon RX 6750 XT",
                16, "GDDR6", 2.618, 2, {"DisplayPort": 3, "HDMI": 1}),
            GraphicsProcessor(
                "Test - XFX", "AMD", "Radeon RX 6600",
                8, "GDDR6", 2.041, 2, {"DisplayPort": 2, "HDMI": 1}),
            GraphicsProcessor(
                "Test - Gigabyte", "NVIDIA", "GeForce RTX 4070",
                12, "GDDR6X", 2.61, 3, {"DisplayPort": 3, "HDMI": 1})
        ]

        self.app = app.test_client()
        self.test_gpu_id = None

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

    def test_add_gpu(self):
        response = self.app.post(
            "/api/gpu/add", data=json.dumps(self.test_gpu.__json__()),
            headers={"Authorization": f"Bearer {self.access_token}"},
            content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.test_gpu_id = response.json['data']['_id']

    def test_add_multiple_gpus(self):
        response = self.app.post(
            "/api/gpu/add/batch", data=json.dumps([gpu.__json__() for gpu in self.test_gpus]),
            headers={"Authorization": f"Bearer {self.access_token}"},
            content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "GPUs added successfully")

    def test_get_all_gpus(self):
        # Get All GPUs from DB
        response = self.app.get("/api/gpu/all", headers={"Authorization": f"Bearer {self.access_token}"})

        self.assertEqual(response.status_code, 200)

    def test_get_gpu_by_id(self):
        self.test_add_gpu()
        url_id = self.test_gpu_id

        response = self.app.get(
            f"/api/gpu/{url_id}", headers={"Authorization": f"Bearer {self.access_token}"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['data']['_id'], url_id)

    def test_get_gpu_by_query(self):
        # Get All GPUs from DB
        response = self.app.get(
            "/api/gpu/filtered/params$brand=Test%20-%20MSI$coprocessor=NVIDIA$architecture=na",
            headers={"Authorization": f"Bearer {self.access_token}"})

        self.assertEqual(response.status_code, 200)

    def test_update_gpu(self):
        self.test_add_gpu()
        url_id = self.test_gpu_id

        mod_gpu_data = {
            "brand": "Test - MSI", "coprocessor": "NVIDIA", "architecture": "GeForce RTX 4080",
            "vram_size": 16, "vram_type": "GDDR6X", "clock_speed": 2.6, "fan_count": 3, "video_outputs": [
                {"HDMI": 2}, {"DisplayPort": 3}]
        }

        response = self.app.put(
            f"/api/gpu/update/{url_id}", data=json.dumps(mod_gpu_data),
            headers={"Authorization": f"Bearer {self.access_token}"},
            content_type="application/json")

        self.assertEqual(response.status_code, 200)

    def test_delete_gpu(self):
        self.test_add_gpu()
        url_id = self.test_gpu_id

        response = self.app.delete(
            f"/api/gpu/delete/{url_id}",
            headers={"Authorization": f"Bearer {self.access_token}"})

        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        # Delete test GPUs marked by Test -
        db.gpus.delete_many({"brand": {"$regex": "^Test - "}})
