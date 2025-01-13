import sounddevice as sd
import wave
import numpy as np
import os
import signal
import datetime

# Parameters
samplerate = 44100  # Hz
channels = 1
current_datetime = datetime.datetime.now()

# Format the date and time as a string (e.g., YYYY-MM-DD_HH-MM-SS)
formatted_datetime = current_datetime.strftime("%Y-%m-%d")

# Create the filename with the date
output_filename = f"audio/recording_{formatted_datetime}.wav"

# Signal handler to stop recording
recording = True

def stop_recording(signum, frame):
    global recording
    recording = False

signal.signal(signal.SIGTERM, stop_recording)

# Open WAV file for writing
with wave.open(output_filename, 'wb') as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(2)
    wf.setframerate(samplerate)

    print("Microphone recording started. Waiting for stop signal...")
    while recording:
        audio = sd.rec(samplerate, samplerate=samplerate, channels=channels, dtype=np.int16)
        sd.wait()
        wf.writeframes(audio.tobytes())

print(f"Microphone recording saved to {output_filename}.")