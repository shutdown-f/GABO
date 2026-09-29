import ollama

MODEL = "qwen2.5:3b-instruct"


class OllamaProvider:
    def __init__(self):
        self.messages = []

    def send(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })

        response = ollama.chat(
            model=MODEL,
            messages=self.messages
        )

        reply = response["message"]["content"]

        self.messages.append({
            "role": "assistant",
            "content": reply
        })

        return reply

    def reset(self):
        self.messages = []

    def info(self):
        return {
            "provider": "Ollama",
            "model": MODEL,
            "status": "LOCAL"
        }


_provider = None


def get_provider():
    global _provider

    if _provider is None:
        _provider = OllamaProvider()

    return _provider


def chat(message):
    return get_provider().send(message)


def reset_chat():
    get_provider().reset()


def provider_info():
    return get_provider().info()