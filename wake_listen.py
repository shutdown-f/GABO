import time

import numpy as np
import sounddevice as sd
from openwakeword.model import Model
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

from gabo_core import think

import subprocess
import sys
import soundfile as sf
from scipy.signal import butter, sosfilt

# =========================
# SETTINGS
# =========================

MIC_DEVICE = 4
SAMPLE_RATE = 16000

WAKE_CHUNK_SIZE = 1280
WAKE_THRESHOLD = 0.5
COOLDOWN = 2.0

SPEECH_THRESHOLD = 0.015
MIN_RECORDING_TIME = 0.5
SILENCE_DURATION = 0.8
MAX_RECORDING_TIME = 15

AUDIO_FILE = "command.wav"

PIPER_MODEL = "en_US-lessac-medium"
TTS_FILE = "gabo_output.wav"
LOWPASS_CUTOFF = 5500


# =========================
# LOAD MODELS
# =========================

print("Loading wake-word detector...")
wake_model = Model()

print("Loading speech recognition...")
stt_model = WhisperModel(
    "tiny.en",
    device="cpu",
    compute_type="int8"
)

print("GABO is ready.")
print("Say: hey Jarvis\n")


# =========================
# RECORD COMMAND
# =========================

def record_command():

    print("Waiting for your command...")

    chunks = []
    speech_started = False
    speech_start_time = None
    last_speech_time = None

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=MIC_DEVICE,
        blocksize=1024,
    ) as stream:

        while True:

            audio, overflowed = stream.read(1024)
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

            # Save audio after speech starts
            if speech_started:

                chunks.append(audio.copy())

                elapsed = now - speech_start_time

                # Maximum recording duration
                if elapsed >= MAX_RECORDING_TIME:

                    print("Maximum recording time reached.")
                    break

                # Stop after silence
                if (
                    last_speech_time is not None
                    and elapsed >= MIN_RECORDING_TIME
                    and now - last_speech_time >= SILENCE_DURATION
                ):

                    print("Silence detected.")
                    break

    if not chunks:

        print("No command detected.")
        return None

    audio = np.concatenate(chunks)

    write(
        AUDIO_FILE,
        SAMPLE_RATE,
        (audio * 32767).astype(np.int16)
    )

    duration = len(audio) / SAMPLE_RATE

    print(f"Command recorded: {duration:.2f} seconds")

    return AUDIO_FILE


# =========================
# SPEECH TO TEXT
# =========================

def transcribe(audio_file):

    print("Transcribing...")

    segments, info = stt_model.transcribe(
        audio_file,
        beam_size=5
    )

    text = " ".join(
        segment.text.strip()
        for segment in segments
    )

    return text

# =========================
#  TEXT TO SPEECH
# =========================

def speak(text):
    print("Generating speech...")

    subprocess.run([
        sys.executable,
        "-m",
        "piper",
        "-m",
        PIPER_MODEL,
        "-f",
        TTS_FILE,
        "--",
        text
    ], check=True)

    print("Applying low-pass filter...")

    audio, sample_rate = sf.read(
        TTS_FILE,
        dtype="float32"
    )

    sos = butter(
        6,
        LOWPASS_CUTOFF,
        btype="lowpass",
        fs=sample_rate,
        output="sos"
    )

    audio = sosfilt(sos, audio)

    print("Speaking...")

    sd.play(audio, sample_rate)
    sd.wait()

    print("Done.")

# =========================
# MAIN LOOP
# =========================
def run():
    # all your existing wake-listen loop goes here
    last_detection = 0

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        device=MIC_DEVICE,
        blocksize=WAKE_CHUNK_SIZE,
    ) as stream:

        while True:

            audio, overflowed = stream.read(WAKE_CHUNK_SIZE)

            audio = np.squeeze(audio)

            prediction = wake_model.predict(audio)

            score = prediction["hey_jarvis"]

            now = time.monotonic()

            # Wake word detected
            if (
                score > WAKE_THRESHOLD
                and now - last_detection > COOLDOWN
            ):

                print(f"\nWAKE DETECTED! score={score:.2f}")

                last_detection = now

                # Record command
                audio_file = record_command()

                if audio_file:

                    # Speech → text
                    text = transcribe(audio_file)

                    print("\nGABO heard:")
                    print(text)

                    # Text → response
                    response = think(text)

                    print("\nGABO:")
                    print(response)

                    speak(response)

                    print("\nGABO is listening again...")
##################
## SELF CALLING ##
##################
if __name__ == "__main__":
    run()