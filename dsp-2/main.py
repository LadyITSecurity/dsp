import pyreaper
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
from scipy.io.wavfile import write
import statsmodels.tsa.stattools as stattools
from scipy.signal.windows import triang


def my_acf(x, m):
    n = len(x)
    u = sum(x[i] for i in range(0, n - 1))
    u = u / n
    r = sum((x[i] - u) * (x[i + m] - u) for i in range(0, n - m - 1))
    r = r / (n - m)
    return r


def test_acf(x):
    acf = np.array([my_acf(x, i) for i in range(0, 6)])
    acf /= acf[0]
    lib_acf = stattools.acf(x, adjusted=True, nlags=5)
    for i in range(6):
        if lib_acf[i] - acf[i] > 1e-05:
            return False
    return True


def draw_acf(x, m):
    acf = stattools.acf(x, adjusted=True, nlags=m)
    plt.figure('ACF')
    plt.plot(acf)
    plt.show()


def google_reaper(x, fs):
    t = np.linspace(0, (len(x) - 1) / fs, len(x))
    # Подготовка данных для reaper
    int16_info = np.iinfo(np.int16)
    x = x * min(int16_info.min, int16_info.max)
    x = x.astype(np.int16)
    # Вызов reaper
    pm_times, pm, f_times, f, _ = pyreaper.reaper(x, fs)
    # Отображение позиций пиков
    plt.figure('[Reaper] Pitch Marks')
    plt.plot(t, x)
    plt.scatter(pm_times[pm == 1], x[(pm_times * fs).astype(int)][pm == 1], marker='x', color='red')
    # Отображение значений основной частоты
    plt.figure('[Reaper] Fundamental Frequency')
    plt.plot(f_times, f)
    print('Average fundamental frequency:', np.mean(f[f != -1]))
    plt.show()


def window(n):
    return triang(n)


def psola(x, fs, k):
    int16_info = np.iinfo(np.int16)
    tmp = x * min(int16_info.min, int16_info.max)
    tmp = tmp.astype(np.int16)
    pm_times, pm, f_times, f, _ = pyreaper.reaper(tmp, fs)
    peaks = pm_times[pm == 1]
    peaks *= fs
    T = round(fs / np.mean(f[f != -1]))
    count = (len(x) - T) // T * 2
    y = np.zeros(round(len(x) * (k + 0.01)))
    w = window(T)
    for i in range(count):
        src_start = i * T // 2
        dst_start = round(src_start * k)
        y[dst_start:dst_start + T] += x[src_start: src_start + T] * w
    return y


def my_dtft(x, fs, f):
    n = np.arange(x.size)
    rel_cyc_f = 2 * np.pi * f / fs
    if hasattr(f, "__len__"):
        f_size = rel_cyc_f.size
        dtft = np.zeros(f_size)
        for i in range(f_size):
            complex_exp = np.exp(-1j * rel_cyc_f[i] * n)
            dtft[i] = abs(np.dot(x, complex_exp))
    else:
        complex_exp = np.exp(-1j * rel_cyc_f * n)
        dtft = abs(np.dot(x, complex_exp))
    return dtft


def draw_dftf(x, fs):
    arg = np.arange(40, 500)
    a = my_dtft(x, fs, arg)

    plt.figure('DTFT')
    plt.plot(arg, a)
    plt.show()


if __name__ == '__main__':
    # Загрузка и нормировка входного сигнала
    fs, x = wavfile.read('input.wav')
    x = x.astype(np.float32)
    x /= max(abs(x.min()), abs(x.max()))
    '''
    print(test_acf(x))
    draw_acf(x, 2000)
    draw_dftf(x, fs)
    google_reaper(x, fs)
    '''

    print('Average fundamental frequency (ACF)\t\t\t', round(44100 / 211))  # 209
    print('Average fundamental frequency (DTFT)\t', 200)
    print('Average fundamental frequency (google REAPER)\t', 203)

    k = 0.85
    res = psola(x, fs, k)
    write('output.wav', fs, res)
