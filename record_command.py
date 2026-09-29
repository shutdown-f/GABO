
import time

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write


# -----------------------------
# Settings
# -----------------------------

MIC_DEVICE = 4
SAMPLE_RATE = 16000

CHUNK_SIZE = 1024

# How loud something must be to count as speech.
# Increase this if background noise triggers recording.
SPEECH_THRESHOLD = 0.025

# Minimum time to record after speech begins.
MIN_RECORDING_TIME = 0.5

# Stop after this much continuous silence.
SILENCE_DURATION = 1.5

# Maximum command length.
MAX_RECORDING_TIME = 15


# -----------------------------
# Recording
# -----------------------------

def record_command():
    print("Waiting for speech...")

    chunks = []
    speech_started = False
    speech_start_time = None
    last_speech_time = None

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=MIC_DEVICE,
        blocksize=CHUNK_SIZE,
    ) as stream:

        while True:
            audio, overflowed = stream.read(CHUNK_SIZE)
            audio = np.squeeze(audio)

            # RMS volume of this chunk
            rms = np.sqrt(np.mean(audio ** 2))

            now = time.monotonic()

            # -----------------------------
            # Detect speech
            # -----------------------------

            if rms > SPEECH_THRESHOLD:

                if not speech_started:
                    print("Speech detected!")
                    speech_started = True
                    speech_start_time = now

                last_speech_time = now

            # -----------------------------
            # Save audio after speech starts
            # -----------------------------

            if speech_started:
                chunks.append(audio.copy())

                elapsed = now - speech_start_time

                # Stop if command gets ridiculously long
                if elapsed >= MAX_RECORDING_TIME:
                    print("Maximum recording time reached.")
                    break

                # Stop after enough silence
                if (
                    last_speech_time is not None
                    and elapsed >= MIN_RECORDING_TIME
                    and now - last_speech_time >= SILENCE_DURATION
                ):
                    print("Silence detected. Recording finished.")
                    break


    if not chunks:
        print("No speech detected.")
        return None

    audio = np.concatenate(chunks)

    write(
        "command.wav",
        SAMPLE_RATE,
        (audio * 32767).astype(np.int16)
    )

    duration = len(audio) / SAMPLE_RATE

    print(f"Saved command.wav ({duration:.2f} seconds)")

    return "command.wav"


# -----------------------------
# Test
# -----------------------------

if __name__ == "__main__":
    record_command()

