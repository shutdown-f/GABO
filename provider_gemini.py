import os

from google import genai


# ============================================================
# GEMINI PROVIDER
# ============================================================

MODEL = "gemini-3.8-flash"


class GeminiProvider:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set.\n"
                "Set it as an environment variable first."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.chat = self.client.chats.create(
            model=MODEL
        )

    # --------------------------------------------------------
    # Send a message
    # --------------------------------------------------------

    def send(self, message):

        response = self.chat.send_message(
            message=message
        )

        return response.text

    # --------------------------------------------------------
    # Reset conversation
    # --------------------------------------------------------

    def reset(self):

        self.chat = self.client.chats.create(
            model=MODEL
        )

    # --------------------------------------------------------
    # Provider information
    # --------------------------------------------------------

    def info(self):

        return {
            "provider": "Google Gemini",
            "model": MODEL,
            "status": "ONLINE"
        }


# ============================================================
# GLOBAL PROVIDER INSTANCE
# ============================================================

_provider = None


def get_provider():

    global _provider

    if _provider is None:
        _provider = GeminiProvider()

    return _provider


def chat(message):

    provider = get_provider()

    return provider.send(message)


def reset_chat():

    provider = get_provider()

    provider.reset()


def provider_info():

    provider = get_provider()

    return provider.info()