import unittest
from user import Database, UserService, User
import os

class TestUserService(unittest.TestCase):
    def setUp(self):
        # Use an in-memory database for testing
        self.db = Database(':memory:')
        self.user_service = UserService(self.db)
    
    def test_create_user(self):
        user_data, status_code = self.user_service.create_user("Alice", 30)
        self.assertEqual(status_code, 201)
        self.assertEqual(user_data["name"], "Alice")
        self.assertEqual(user_data["age"], 30)
    
    def test_get_user(self):
        user_data, _ = self.user_service.create_user("Bob", 25)
        user_id = user_data["user_id"]
        retrieved_user, status_code = self.user_service.get_user(user_id)
        self.assertEqual(status_code, 200)
        self.assertEqual(retrieved_user["name"], "Bob")
        self.assertEqual(retrieved_user["age"], 25)
    
    def test_get_nonexistent_user(self):
        retrieved_user, status_code = self.user_service.get_user(999)
        self.assertEqual(status_code, 404)
        self.assertEqual(retrieved_user["error"], "User not found")
    
    def test_user_class(self):
        """Test the User class constructor"""
        user = User(1, "Charlie", 40)
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.name, "Charlie")
        self.assertEqual(user.age, 40)

    def test_update_user(self):
        user_data, _ = self.user_service.create_user("David", 28)
        user_id = user_data["user_id"]
        self.db.update_user(user_id, "David Updated", 29)
        updated_user, status_code = self.user_service.get_user(user_id)
        self.assertEqual(status_code, 200)
        self.assertEqual(updated_user["name"], "David Updated")
        self.assertEqual(updated_user["age"], 29)

    def test_delete_user(self):
        user_data, _ = self.user_service.create_user("Eve", 35)
        user_id = user_data["user_id"]
        self.db.delete_user(user_id)
        deleted_user, status_code = self.user_service.get_user(user_id)
        self.assertEqual(status_code, 404)
        self.assertEqual(deleted_user["error"], "User not found")

if __name__ == "__main__":
    unittest.main()
