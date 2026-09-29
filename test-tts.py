#```python
import subprocess
import sys

import sounddevice as sd
import soundfile as sf
from scipy.signal import butter, sosfilt


MODEL = "en_US-lessac-medium"
OUTPUT = "gabo_output.wav"
LOWPASS_CUTOFF = 5500  # Hz


def lowpass(audio, sample_rate, cutoff=LOWPASS_CUTOFF):
    """Apply a gentle low-pass filter to the generated voice."""
    sos = butter(
        6,
        cutoff,
        btype="lowpass",
        fs=sample_rate,
        output="sos"
    )

    return sosfilt(sos, audio)


def speak(text):
    print("Generating speech...")

    # Use the same Python interpreter running this script.
    subprocess.run([
        sys.executable,
        "-m",
        "piper",
        "-m",
        MODEL,
        "-f",
        OUTPUT,
        "--",
        text
    ], check=True)

    print("Applying low-pass filter...")

    audio, sample_rate = sf.read(
        OUTPUT,
        dtype="float32"
    )

    audio = lowpass(
        audio,
        sample_rate
    )

    print("Speaking...")

    sd.play(audio, sample_rate)
    sd.wait()

    print("Done.")


if __name__ == "__main__":
    speak("This is GABO speaking, Over!")
#```
