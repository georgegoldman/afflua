class MockedGenerativeAI:
    def __init__(self, response_text):
        self.response_text = response_text

    def generate_content(self, message):
        completion = type("", (), {"text": self.response_text})
        return completion