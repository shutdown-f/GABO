import sounddevice as sd
import numpy as np
import time
from openwakeword.model import Model

MIC_DEVICE = 4
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280
THRESHOLD = 0.5
COOLDOWN = 2.0

print("Loading wake-word detector...")
model = Model()

print("Listening for 'hey jarvis'...")
print("Press Ctrl+C to stop.")

last_detection = 0

with sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16",
    device=MIC_DEVICE,
    blocksize=CHUNK_SIZE
) as stream:

    while True:
        audio, overflowed = stream.read(CHUNK_SIZE)
        audio = np.squeeze(audio)

        prediction = model.predict(audio)
        score = prediction["hey_jarvis"]

        now = time.monotonic()

        if score > THRESHOLD and now - last_detection > COOLDOWN:
            print(f"WAKE DETECTED! score={score:.2f}")
            last_detection = now