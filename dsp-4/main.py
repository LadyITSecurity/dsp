import scipy
from scipy.io import wavfile
from scipy.io.wavfile import write
from scipy.signal import stft, istft, get_window
import matplotlib.pyplot as plt
import numpy as np


def main():
    fs, x = wavfile.read('input2.wav')
    # time = 0.2
    # name = 'triangle'
    # size = round(time * fs)
    # window = get_window(name, size)
    # f, t, spectrum = stft(x, fs, window=window, nperseg=size)
    f, t, spectrum = stft(x, fs, nperseg=round(0.04 * fs))
    result, what = istft(abs(spectrum), nperseg=round(0.04 * fs))
    what /= max(abs(what.min()), abs(what.max()))
    write('output.wav', fs, what)
    plt.figure('spectorgram')
    plt.pcolormesh(t, f, np.log(np.abs(spectrum) + 1))
    plt.xlabel('sec')
    plt.ylabel('Hz')
    plt.show()


if __name__ == '__main__':
    main()
