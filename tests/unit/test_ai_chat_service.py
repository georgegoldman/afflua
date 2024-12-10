import unittest
from unittest.mock import patch

from aleaf.schemas.ai_chat import ChatResponse
from aleaf.services.ai_chat_service import generate_ai_response

# Import mocked version of google.generativeai
from tests.mocks.generativeai import MockedGenerativeAI


class TestAIChatService(unittest.TestCase):
    @patch('aleaf.services.ai_chat.genai.GenerativeModel', MockedGenerativeAI("This is a generated response"))
    async def test_generated_ai_response_success(self):
        context = "Hi there! How can I help you today?"
        user_message = "I'm looking for information on AI chatbots."

        response = await generate_ai_response(context, user_message)

        self.assertIsInstance(response, ChatResponse)
        self.assertEqual(response.response, "This is a generated response")

    @patch('aleaf.services.ai_chat.genai.GenerativeModel.generate_content', side_effect=Exception("Mocked Exception"))
    async def test_generate_ai_response_exception(self):
        context = None
        user_message = "How's the weather?"

        response = await generate_ai_response(context, user_message)

        self.assertIsInstance(response, str)
        self.assertTrue(response.startswith("Error:"))
