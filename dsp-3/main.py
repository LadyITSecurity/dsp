import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.io.wavfile import write
from scipy import interpolate as inter


def shift(x, fs, dt, at, f):
    t = np.linspace(0, (len(x) - 1) / fs, len(x))
    new_t = np.zeros(len(t))
    new_t = t + dt + at * np.sin(2 * np.pi * f * t)
    f = inter.interp1d(t, x, kind="linear")
    new_x = np.zeros(int(len(new_t)))
    max_t = max(t)
    new_x = [f(new_t[i]) if new_t[i] < max_t else 0 for i in range(len(new_t))]
    '''
    plt.plot(x)
    plt.show()
    plt.plot(new_x)
    plt.show()
    '''
    return new_x


def main():
    n = 3
    file = 'input.wav'
    fs, x = wavfile.read(file)
    x = x.astype(np.float32)
    x /= max(abs(min(x)), abs(max(x)))
    t = np.linspace(0, (len(x) - 1) / fs, len(x))
    y = x.copy()
    y = x.astype(np.float32) / x.max()
    for i in range(n):
        y += np.float32(shift(x, fs, 0.005*(i+1), 0.01, 3))
    y /= y.max()
    write("horus.wav", fs, y)


if __name__ == '__main__':
    main()
