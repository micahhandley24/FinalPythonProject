import os
import numpy as np
import soundfile as sf
from scipy.signal import find_peaks
from tkinter import Tk, Button, Label, filedialog, Frame
import matplotlib.pyplot as plt
from pydub import AudioSegment
import pandas as pd

class AudioAnalyzer:
    def __init__(self, root):
        self.root = root
        self.file_path = None
        self.audio_data = None
        self.sample_rate = None

        # GUI Layout
        self.label = Label(root, text="Load an audio file", font=("Arial", 14))
        self.label.pack()

        self.load_button = Button(root, text="Load File", command=self.load_file)
        self.load_button.pack()

        self.clean_button = Button(root, text="Clean and Process Audio", command=self.clean_audio, state="disabled")
        self.clean_button.pack()

        self.analysis_button = Button(root, text="Analyze Data", command=self.analyze_audio, state="disabled")
        self.analysis_button.pack()

        self.visualize_button = Button(root, text="Visualize Data", command=self.visualize_data, state="disabled")
        self.visualize_button.pack()

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.aac")])
        if self.file_path:
            self.label.config(text=f"Loaded: {os.path.basename(self.file_path)}")
            if not self.file_path.endswith(".wav"):
                self.convert_to_wav()
            else:
                self.clean_button.config(state="normal")

    def convert_to_wav(self):
        sound = AudioSegment.from_file(self.file_path)
        self.file_path = self.file_path.rsplit(".", 1)[0] + ".wav"
        sound.export(self.file_path, format="wav")
        self.label.config(text=f"Converted to WAV: {os.path.basename(self.file_path)}")
        self.clean_button.config(state="normal")

    def clean_audio(self):
        # Read WAV file
        self.audio_data, self.sample_rate = sf.read(self.file_path)

        # Handle multi-channel audio
        if len(self.audio_data.shape) > 1:
            self.audio_data = np.mean(self.audio_data, axis=1)

        # Remove metadata
        self.label.config(text=f"Audio cleaned: {os.path.basename(self.file_path)}")
        self.analysis_button.config(state="normal")

    def analyze_audio(self):
        if self.audio_data is None:
            return

        duration = len(self.audio_data) / self.sample_rate
        peaks, _ = find_peaks(self.audio_data, height=np.max(self.audio_data) * 0.8)
        highest_resonant_freq = self.sample_rate / len(peaks) if len(peaks) > 0 else 0

        # Placeholder for RT60 (requires detailed room acoustics computation)
        rt60 = duration * 0.6

        # Data summary
        self.summary = {
            "Duration (s)": duration,
            "Highest Resonant Frequency (Hz)": highest_resonant_freq,
            "RT60 (s)": rt60
        }

        self.label.config(text=f"Analysis Complete. Duration: {duration:.2f}s, Freq: {highest_resonant_freq:.2f}Hz, RT60: {rt60:.2f}s")
        self.visualize_button.config(state="normal")

    def visualize_data(self):
        if self.audio_data is None:
            return

        time = np.linspace(0, len(self.audio_data) / self.sample_rate, num=len(self.audio_data))

        # Waveform plot
        plt.figure(figsize=(10, 4))
        plt.plot(time, self.audio_data)
        plt.title("Waveform")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.show()

        # RT60 Visualization (Placeholder)
        rt60_values = [self.summary["RT60 (s)"] / 3] * 3  # Low, Mid, High (Placeholder)
        plt.figure(figsize=(10, 4))
        plt.bar(["Low", "Mid", "High"], rt60_values, color=['blue', 'green', 'red'])
        plt.title("RT60 Values Across Frequency Ranges")
        plt.ylabel("RT60 (s)")
        plt.show()

        # Histogram of amplitude
        plt.figure(figsize=(10, 4))
        plt.hist(self.audio_data, bins=50, color='gray', edgecolor='black')
        plt.title("Amplitude Distribution")
        plt.xlabel("Amplitude")
        plt.ylabel("Frequency")
        plt.show()


# Main Application
if __name__ == "__main__":
    root = Tk()
    root.title("Audio Analyzer")
    app = AudioAnalyzer(root)
    root.mainloop()
