import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import firls, convolve, freqz
from scipy.fft import fft


def main():
    x = np.load("13.npy")

    plt.figure('input', figsize=(20, 1))
    plt.plot(x)

    spectre = fft(x)

    plt.figure('input spectre')
    plt.plot(np.abs(spectre[:round(len(spectre)/2)]))
    plt.show()

    f = 131
    omega = f * np.pi/len(x)
    samples = np.pi / (2 * omega)
    # print(omega)
    # print(samples)
    m = np.ceil(samples)
    freq = 1 / m
    # print(freq)

    # 3
    h = firls(m, [0, freq, freq, 1], [1, 1, 0, 0])
    h_padded = np.pad(h, (0, 9 * len(h)))
    spectre_h = np.abs(fft(h_padded))
    spectre_h = spectre_h[:len(spectre_h) // 2]
    plt.figure('frequency response')
    plt.plot(spectre_h)

    # 4
    result = convolve(x, h)
    plt.figure("reconstructed", figsize=(20, 1))
    plt.plot(result)
    np.save("13f.npy", result)
    plt.show()


if __name__ == '__main__':
    main()
