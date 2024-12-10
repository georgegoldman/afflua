import unittest
from unittest.mock import patch

from aleaf.services.user_service import create_user, get_user_by_id, update_user, delete_user
from aleaf.schemas.user import UserCreate, UserResponse

class TestUserService(unittest.TestCase):

    @patch('aleaf.services.user_service.collection.insert_one')
    async def test_create_user(self, mock_insert_one):
        user_data = UserCreate(username='john_doe', email='john@example.com', password='password123')

        mock_insert_one.return_value = {'inserted_id': 'some_id'}

        result = await create_user(user_data)

        mock_insert_one.assert_called_once_with(user_data.model_dump())
        self.assertEqual(result.id, 'some_id')

    @patch('aleaf.services.user_service.collection.find_one')
    async def test_get_user(self, mock_find_one):
        expected_user_data = {"username": "john_doe", "email": "john@example.com"}
        mock_find_one.return_value =  expected_user_data

        user_id = "some_id"
        result = await get_user_by_id(user_id)

        self.assertEqual(result, expected_user_data)

        mock_find_one.return_value = None

        result = await get_user_by_id(user_id)

        self.assertIsNone(result)

    @patch('aleaf.services.user_service.collection.update_user')
    async def test_update_user(self, mock_update_user):
        user_id = "some_id"
        update_data = {"email": "new_email@example.com"}

        mock_update_user.return_value = {"modified_count": 1}
        result = await update_user(user_id, update_data)

        self.assertTrue(result) # Assuming a boolean indicating success

        mock_update_user.side_effect = Exception("Update failed")
        with self.assertRaises(Exception):
            await update_user(user_id, update_data)

    @patch('aleaf.services.user_service.collection.delete_user')
    async def test_delete_user(self, mock_delete_user):
        user_id = "some_id"

        mock_delete_user.return_value = {"deleted_count": 1}
        result = await delete_user(user_id)

        self.assertTrue(result) # Assuming a boolean indicating success

        mock_delete_user.side_effect = Exception("Delete failed")
        with self.assertRaises(Exception):
            await delete_user(user_id)