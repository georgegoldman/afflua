from aleaf.schemas.ai_chat import ChatResponse
from typing import Optional
from aleaf.core.config import settings
from datetime import datetime

import google.generativeai as genai #type: ignore


api_key = settings.AI_API_KEY
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


async def generate_ai_response(context: Optional[str], user_message: str) -> ChatResponse:

    message = []
    if context:
        message.append({"role": "system", "content": context})
    message.append({"role": "user", "content": str(message)})

    try:
        completion = model.generate_content(message)
        response = completion.text
        return ChatResponse(response=response, timestamp=str(datetime.now()))
    except Exception as e:
        return f"Error: {str(e)}" #type: ignore