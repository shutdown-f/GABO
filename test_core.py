def think(text):
    text = text.lower().strip()

    if "hello" in text or "hi" in text:
        return "Hello. I am GABO."

    if "your name" in text:
        return "GABO. Obviously."

    if "time" in text:
        return "I don't know the time yet."

    return f"You said: {text}"