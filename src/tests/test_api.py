import unittest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.getcwd())
from main import app
from databases.database import create_db, drop_db


class TestTask(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)


    def test_api(self):
        # Register User
        response_register = self.client.post(
            "/users/me/",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            json={"name": "admin", "email": 'admin@mail.com', "password": "admin123"},
        )
        self.assertEqual(response_register.status_code, 200)

        # Login User
        response_login = self.client.post(
            "/token",
            headers={"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
            content="grant_type=password&username=admin@mail.com&password=admin123&scope=&client_id=&client_secret="
        )
        self.assertEqual(response_login.status_code, 200)
        self.access_token = response_login.json()['access_token']

        # Test Create Task
        response_create = self.client.post(
            "/api/v1/tasks/",
            headers={
                "Accept": "application/json", 
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}"
            },
            json={
                "name": "mytask", 
                "description": "description of my task", 
                "status": "pending"
            },
        )
        self.assertEqual(response_create.status_code, 200)
        self.assertEqual(response_create.json()['name'], 'mytask')
        self.task_id = response_create.json()['id']

        # Test Get a Task
        response_get = self.client.get(
            f"/api/v1/tasks/{self.task_id}",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.access_token}"
            },
        )
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_get.json()['name'], 'mytask')
    

if __name__ == '__main__':
    drop_db()  # Drop database finished
    create_db()  # Create database
    unittest.main()
