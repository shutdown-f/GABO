import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
DURATION = 10
MIC_DEVICE = 4

print("Loading GABO's speech recognition...")
model = WhisperModel(
    "tiny.en",
    device="cpu",
    compute_type="int8"
)

print("Speak now...")
audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16",
    device=MIC_DEVICE
)

sd.wait()

write("test.wav", SAMPLE_RATE, audio)

print("Transcribing...")

segments, info = model.transcribe(
    "test.wav",
    beam_size=5
)

text = " ".join(segment.text.strip() for segment in segments)

print()
print("GABO heard:")
print(text)