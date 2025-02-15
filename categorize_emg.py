import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq

def load_emg_data(file_path):
    df = pd.read_csv(file_path)
    print("Timestamp data before conversion:", df["Timestamp"].head())  # debugging
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])   
    time = (df["Timestamp"] - df["Timestamp"].iloc[0]).dt.total_seconds()
    emg_signal = df["Data"].values
    return time, emg_signal

def compute_fft(time, emg_signal):
    N = len(emg_signal)
    dt = np.mean(np.diff(time))
    print("dt:", dt)  # debugging
    fft_values = fft(emg_signal)
    print("FFT values:", fft_values)  # debugging
    frequencies = fftfreq(N, dt)
    print("Frequencies:", frequencies)  # debugging
    power_spectrum = np.abs(fft_values) ** 2
    print("Power spectrum:", power_spectrum)  # debugging
    positive_freqs = frequencies[:N // 2]
    positive_power = power_spectrum[:N // 2]
    dominant_freq_index = np.argmax(positive_power)
    dominant_freq = positive_freqs[dominant_freq_index]

    return dominant_freq, positive_freqs, positive_power

def categorize_tremor(dominant_freq):
    if 3 <= dominant_freq < 7:
        return "Resting Tremor (3-7 Hz)"
    elif 4 <= dominant_freq < 9:
        return "Postural Tremor (4-9 Hz)"
    elif 7 <= dominant_freq < 12:
        return "Kinetic Tremor (7-12 Hz)"
    else:
        return "No Tremor Detected (Outside expected frequency range)"

def plot_results(time, emg_signal, positive_freqs, positive_power, dominant_freq):
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(time, emg_signal, color="blue")
    plt.xlabel("Time (s)")
    plt.ylabel("EMG Signal (μV)")
    plt.title("Raw EMG Signal")

    plt.subplot(1, 2, 2)
    plt.plot(positive_freqs, positive_power, color="red")
    plt.axvline(x=dominant_freq, color="green", linestyle="--", label=f"Peak Frequency: {dominant_freq:.2f} Hz")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power (Amplitude²)")
    plt.title("Frequency vs. Power Spectrum")
    plt.legend()

    plt.tight_layout()
    plt.show()

def main():
    emg_file = "data/arduino_data_with_time.csv"
    
    time, emg_signal = load_emg_data(emg_file)
    
    print("Time data:", time)
    print("EMG Signal data:", emg_signal)

    dominant_freq, positive_freqs, positive_power = compute_fft(time, emg_signal)

    tremor_type = categorize_tremor(dominant_freq)
    print(f"Detected Tremor Frequency: {dominant_freq:.2f} Hz")
    print(f"Tremor Classification: {tremor_type}")

    plot_results(time, emg_signal, positive_freqs, positive_power, dominant_freq)

if __name__ == "__main__":
    main()