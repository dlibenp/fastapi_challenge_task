import unittest
from fastapi.testclient import TestClient
import random
import string
import sys
import os
sys.path.append(os.getcwd())
from main import app, metadata_db_migrations as db
from utils import crud
from models import models


class TestTask(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_task(self):
        # Register User
        characters = string.ascii_letters + string.digits
        email_name = ''.join(random.choices(characters, k=10))
        resp_register = self.client.post(
            "/users/me/",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            json={"name": "admin", "email": f"e{email_name}@mail.com", "password": "admin123"},
        )
        self.assertEqual(resp_register.status_code, 200)

        resp_login = self.client.post(
            "/token",
            headers={"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
            content=f"grant_type=password&username=e{email_name}@mail.com&password=admin123&scope=&client_id=&client_secret="
        )
        self.assertEqual(resp_login.status_code, 200)
        access_token = resp_login.json()['access_token']
        
        # # Test Create Task
        resp_task = self.client.post(
            "/api/v1/tasks/",
            headers={
                "Accept": "application/json", 
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
            json={
                "name": "mytask", 
                "description": "description of my task", 
                "status": "pending"
            },
        )
        self.assertEqual(resp_task.status_code, 200)
        self.assertEqual(resp_task.json()['name'], 'mytask')
        task_id = resp_task.json()['id']

        # # Test Get a Task
        response = self.client.get(
            f"/api/v1/tasks/{task_id}",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'mytask')


if __name__ == '__main__':
    unittest.main()



# class TestTaskAPI(unittest.TestCase):  
#     def setUp(self):  
#         self.client = TestClient(app)  
#         app.tasks = []  # Reset tasks before each test  
#         app.users_db = {}  # Reset users before each test  

#         # Register a user and obtain an access token  
#         self.base_username = "testuser"  
#         self.password = "password"  
#         self.register_user(self.base_username, self.password)  

#         # Obtain the access token  
#         self.token = self.get_access_token()  

#     def register_user(self, username, password):  
#         response = self.client.post("/register", json={"username": username, "password": password})  
#         self.assertEqual(response.status_code, 200)  
#         self.username = response.json()["username"]  # Store the unique username  

#     def get_access_token(self):  
#         response = self.client.post("/token", data={"username": self.username, "password": self.password})  
#         return response.json()["access_token"]  

#     def test_create_task(self):  
#         response = self.client.post("/tasks/", json={"id": 1, "title": "Test Task", "description": "Testing task creation"}, headers={"Authorization": f"Bearer {self.token}"})  
#         self.assertEqual(response.status_code, 200)  
#         self.assertEqual(response.json(), {"id": 1, "title": "Test Task", "description": "Testing task creation"})  

#     def test_get_tasks(self):  
#         self.client.post("/tasks/", json={"id": 1, "title": "Test Task", "description": "Testing task creation"}, headers={"Authorization": f"Bearer {self.token}"})  
#         response = self.client.get("/tasks/", headers={"Authorization": f"Bearer {self.token}"})  
#         self.assertEqual(response.status_code, 200)  
#         self.assertEqual(len(response.json()), 1)  

#     def test_get_task(self):  
#         self.client.post("/tasks/", json={"id": 1, "title": "Test Task", "description": "Testing task creation"}, headers={"Authorization": f"Bearer {self.token}"})  
#         response = self.client.get("/tasks/1", headers={"Authorization": f"Bearer {self.token}"})  
#         self.assertEqual(response.status_code, 200)  
#         self.assertEqual(response.json(), {"id": 1, "title": "Test Task", "description": "Testing task creation"})  

#     def test_get_task_not_found(self):  
#         response = self.client.get("/tasks/999", headers={"Authorization": f"Bearer {self.token}"})  
#         self.assertEqual(response.status_code, 404)  
#         self.assertEqual(response.json(), {"detail": "Task not found"})  

#     def test_update_task(self):  
#         self.client.post("/tasks/", json={"id": 1, "title": "Test Task", "description": "Testing task creation"}, headers={"Authorization": f"Bearer {self.token}"})  
#         response = self.client.put("/tasks/1", json={"id": 1, "title": "Updated Task", "description": "Updated description"}, headers={"Authorization": f"Bearer {self.token}"})  
#         self.assertEqual(response.status_code, 200)  
#         self.assertEqual(response.json(), {"id": 1, "title": "Updated Task", "description": "Updated description"})  

#     def test_delete_task(self):  
#         self.client.post("/tasks/", json={"id": 1, "title": "Test Task", "description": "Testing task creation"}, headers={"Authorization": f"Bearer {self.token}"})  
#         response = self.client.delete("/tasks/1", headers={"Authorization": f"Bearer {self.token}"})  
#         self.assertEqual(response.status_code, 200)  
#         self.assertEqual(response.json(), {"detail": "Task deleted"})  
#         response = self.client.get("/tasks/1", headers={"Authorization": f"Bearer {self.token}"})  
#         self.assertEqual(response.status_code, 404)  
