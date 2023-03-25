from scipy.io import wavfile
from scipy.signal import stft
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window


notes = {
    'C2': 65.40639,    'D2': 73.41619,    'E2': 82.40689,    'F2': 87.30706,    'G2': 97.99886,    'A2': 110.0000,    'B2': 116.5409,
    'C3': 130.8128,    'D3': 146.8324,    'E3': 164.8138,    'F3': 174.6141,    'G3': 195.9977,    'A3': 220.0000,    'B3': 246.9417,
    'C4': 261.6256,    'C4#': 277.1826,   'D4': 293.6648,    'D4#': 311.1270,   'E4': 329.6276,    'F4': 349.2282,    'F4#': 369.9944,   'G4': 391.9954,    'G4#': 415.3047,   'A4': 440.0000,    'A4#': 466.1638,   'B4': 493.8833,
    'C5': 523.2511,    'C5#': 554.3653,   'D5': 587.3295,    'D5#': 622.2540,   'E5': 659.2551,    'F5': 698.4565,    'F5#': 739.9888,   'G5': 783.9909,    'G5#': 830.6094,   'A5': 880.0000,    'A5#': 932.3275,   'B5': 987.7666,
    '': 0
}

def main():
    fs, x = wavfile.read('lab5_13.wav')
    x = x[:, 0]
    x = x.astype(np.float32)
    x /= max(abs(x.min()), abs(x.max()))

    time = 0.2
    name = 'triangle'
    size = round(time * fs)
    window = get_window(name, size)
    f, t, zxx = stft(x, fs, window=window, nperseg=size)
    # print(zxx.shape)
    # plt.figure('spectorgram')
    # plt.pcolormesh(t, f, np.abs(zxx)**2)
    # plt.xlabel('sec')
    # plt.ylabel('Hz')
    # plt.show()

    max_f = [[0.0, 0.0] * len(zxx[0])] * len(zxx[0])
    for i in range(len(zxx[0])):
        max_value = abs(zxx[0][i])
        ind = 0
        for j in range(len(zxx)):
            if abs(zxx[j][i]) > max_value:
                ind = j
                max_value = abs(zxx[j][i])
        max_f[i] = [f[ind], max_value]
    o = 0
    for i in max_f:
        print(o, '\t', i[0], '\t', i[1])
        o += 1

    f = max_f[0][0]
    max_value = max_f[0][1]
    score_value = []
    score_f = []
    k = 0

    for i in range(len(max_f)):
        if max_f[i][1] < 0.02:
            if f != 0:
                k += 1
                f, max_value = 0, 0
                score_f.append(0)
                score_value.append([0])
            else:
                score_value[k].append(0)
        elif max_f[i][0] == f:
            if i == 0:
                score_f.append(max_f[i][0])
                score_value.append([max_f[i][1]])
            elif max_f[i][1] > max_value: # or max_f[i][1] - max_f[i-1][1] < 0.1:
                if abs(i - score_value[k].index(max_value)) > 2:
                    k += 1
                    score_f.append(max_f[i][0])
                    score_value.append([max_f[i][1]])
                else:
                    score_value[k].append(max_f[i][1])
                max_value = max_f[i][1]
            else:
                score_value[k].append(max_f[i][1] if max_f[i][1] > 0.02 else 0)
        else:
            k += 1
            f = max_f[i][0]
            max_value = max_f[i][1]
            score_f.append(max_f[i][0] if max_f[i][1] > 0.02 else 0)
            score_value.append([max_f[i][1]])

    for note in score_value:
        max_first = max(note)
        max_second = min(note)
        for i in note:
            if i > max_second:
                max_second = i

    histogram = []
    for i in score_value:
        histogram.append(len(i))

    for i in range(len(histogram)):
        print(score_f[i], '\t', histogram[i], '\t', score_value[i])


    # quarter = histogram.index(max(histogram))
    # eighth = quarte // 1


    score = []
    # 1 - частота
    # 2 - длительность
    # for i in range[score_value]:
    #     duration = len(i)

    plt.figure('HISTOGRAM')
    x = [histogram.count(histogram[i]) for i in range(len(histogram))]
    plt.xlabel('duration')
    plt.ylabel('count of elements')
    plt.grid(which='major', color='gray')
    plt.minorticks_on()
    plt.grid(which='minor', color='gray', linestyle=':')
    plt.bar(histogram, x)
    plt.show()


if __name__ == '__main__':
    main()