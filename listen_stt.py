import time

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel


# -----------------------------
# Settings
# -----------------------------

MIC_DEVICE = 4
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024

SPEECH_THRESHOLD = 0.015
MIN_RECORDING_TIME = 0.5
SILENCE_DURATION = 0.8
MAX_RECORDING_TIME = 15

AUDIO_FILE = "command.wav"


# -----------------------------
# Load Whisper
# -----------------------------

print("Loading speech recognition...")

model = WhisperModel(
    "tiny.en",
    device="cpu",
    compute_type="int8"
)

print("Whisper ready.")


# -----------------------------
# Record command
# -----------------------------

def record_command():

    print("\nWaiting for speech...")

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

            rms = np.sqrt(np.mean(audio ** 2))
            now = time.monotonic()

            # Detect speech
            if rms > SPEECH_THRESHOLD:

                if not speech_started:
                    print("Speech detected!")
                    speech_started = True
                    speech_start_time = now

                last_speech_time = now

            # Store audio after speech begins
            if speech_started:

                chunks.append(audio.copy())

                elapsed = now - speech_start_time

                # Maximum command length
                if elapsed >= MAX_RECORDING_TIME:
                    print("Maximum recording time reached.")
                    break

                # Silence means command is finished
                if (
                    last_speech_time is not None
                    and elapsed >= MIN_RECORDING_TIME
                    and now - last_speech_time >= SILENCE_DURATION
                ):
                    print("Silence detected.")
                    break

    if not chunks:
        print("No speech detected.")
        return None

    audio = np.concatenate(chunks)

    write(
        AUDIO_FILE,
        SAMPLE_RATE,
        (audio * 32767).astype(np.int16)
    )

    duration = len(audio) / SAMPLE_RATE

    print(f"Recorded {duration:.2f} seconds.")

    return AUDIO_FILE


# -----------------------------
# Transcribe
# -----------------------------

def transcribe(audio_file):

    print("Transcribing...")

    segments, info = model.transcribe(
        audio_file,
        beam_size=5
    )

    text = " ".join(
        segment.text.strip()
        for segment in segments
    )

    return text


# -----------------------------
# Test
# -----------------------------

if __name__ == "__main__":

    audio_file = record_command()

    if audio_file:

        text = transcribe(audio_file)

        print("\nGABO heard:")
        print(text)