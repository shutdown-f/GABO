import os
from groq import Groq

MODEL = "openai/gpt-oss-20b"


class GroqProvider:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set.\n"
                "Set it as a Windows environment variable first."
            )

        self.client = Groq(api_key=api_key)
        self.messages = []

    def send(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })

        response = self.client.chat.completions.create(
            model=MODEL,
            messages=self.messages
        )

        reply = response.choices[0].message.content

        self.messages.append({
            "role": "assistant",
            "content": reply
        })

        return reply

    def reset(self):
        self.messages = []

    def info(self):
        return {
            "provider": "Groq",
            "model": MODEL,
            "status": "ONLINE"
        }


_provider = None


def get_provider():
    global _provider

    if _provider is None:
        _provider = GroqProvider()

    return _provider


def chat(message):
    return get_provider().send(message)


def reset_chat():
    get_provider().reset()


def provider_info():
    return get_provider().info()