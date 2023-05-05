import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import wave
import pyaudio
import tkinter as tk
from tkinter import filedialog
import threading
from threading import Thread
import time


CHUNK_SIZE = 1024

def init(line):
    line.set_data([], [])
    return line,

def update(frame_number, line, time_values, data, ax):
    playback_end_position = frame_number * CHUNK_SIZE
    line.set_data(time_values[:playback_end_position], data[:playback_end_position])
    ax.set_xlim(time_values[0], time_values[min(playback_end_position, len(data) - 1)])
    return line,



def plot_waveform(file_path):
    with wave.open(file_path, 'rb') as wav:
        n_frames = wav.getnframes()
        sample_rate = wav.getframerate()
        width = wav.getsampwidth()

        # Read the entire file into data
        raw_data = wav.readframes(n_frames)
        data = np.frombuffer(raw_data, dtype=np.int16 if width == 2 else np.int8)

    fig, ax = plt.subplots()
    ax.plot(data)
    plt.show(block=False)

    def play_audio():
        p = pyaudio.PyAudio()

        with wave.open(file_path, 'rb') as wav:
            stream = p.open(format=p.get_format_from_width(wav.getsampwidth()),
                            channels=wav.getnchannels(),
                            rate=wav.getframerate(),
                            output=True)

            CHUNK = 1024
            data = wav.readframes(CHUNK)

            while data:
                stream.write(data)
                data = wav.readframes(CHUNK)

            stream.stop_stream()
            stream.close()

        p.terminate()

    audio_thread = Thread(target=play_audio)
    audio_thread.start()


def select_wav_file():
    file_path = filedialog.askopenfilename(title="Select a .wav file", filetypes=[("WAV files", "*.wav")])

    if file_path:
        plot_waveform(file_path)
    else:
        print("No file selected.")

def main():
    root = tk.Tk()
    root.title("WaveForm Visualizer")

    label = tk.Label(root, text="Welcome to WaveForm Visualizer")
    label.pack(pady=20)

    select_button = tk.Button(root, text="Select Wav File", command=select_wav_file)
    select_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
