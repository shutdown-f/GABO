from provider_ollama import chat


def think(text):
    return chat(text)

def think_legacy(text):
    text = text.lower().strip()

    if "hello" in text or "hi" in text:
        return "Hello. I am GABO."

    if "your name" in text:
        return "GABO. Obviously."

    if "how are you" in text:
        return "Operational. Mostly."

    if "time" in text:
        return "I do not have access to the clock yet."

    if "who are you" in text:
        return "I am GABO, your personal assistant."

    return f"You said: {text}"