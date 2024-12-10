import unittest
from unittest.mock import patch

from aleaf.services.user_service import create_user, get_user_by_id
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