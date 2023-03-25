# This is a sample Python script.
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from scipy import signal
from scipy.io.wavfile import write


notes = {
    'C2': 65.40639,    'D2': 73.41619,    'E2': 82.40689,    'F2': 87.30706,    'G2': 97.99886,    'A2': 110.0000,    'B2': 116.5409,
    'C3': 130.8128,    'D3': 146.8324,    'E3': 164.8138,    'F3': 174.6141,    'G3': 195.9977,    'A3': 220.0000,    'B3': 246.9417,
    'C4': 261.6256,    'C4#': 277.1826,   'D4': 293.6648,    'D4#': 311.1270,   'E4': 329.6276,    'F4': 349.2282,    'F4#': 369.9944,   'G4': 391.9954,    'G4#': 415.3047,   'A4': 440.0000,    'A4#': 466.1638,   'B4': 493.8833,
    'C5': 523.2511,    'C5#': 554.3653,   'D5': 587.3295,    'D5#': 622.2540,   'E5': 659.2551,    'F5': 698.4565,    'F5#': 739.9888,   'G5': 783.9909,    'G5#': 830.6094,   'A5': 880.0000,    'A5#': 932.3275,   'B5': 987.7666,
    '': 0
}

score_le_onde = [
    'A2', 'E3', 'A3', 'B3', 'C4', 'E4', 'A2', 'E3', 'A3', 'B3', 'C4', 'E4',
    'F2', 'C3', 'A3', 'B3', 'C4', 'E4', 'G2', 'D3', 'A3', 'B3', 'C4', 'E4',
    'A2', 'E3', 'A3', 'B3', 'C4', 'E4', 'A2', 'E3', 'A3', 'B3', 'C4', 'E4',
    'F2', 'C3', 'A3', 'B3', 'C4', 'E4', 'G2', 'D3', 'A3', 'B3', 'C4', 'E4',
]

score_raffaello = [
    'D4', '', 'E4', 'F4#', 'D4', 'C4#', '', 'D4', 'E4', 'F4#', 'F4#', '', 'G4', 'A4', 'B4', 'E4', '', '',
    'F4', '', 'F4#', 'G4', 'A4', 'D5', '', 'C5#', 'B4', 'F4#', 'A4', '', '', 'G4#', 'G4', '', '',
    'D4', '', 'E4', 'F4#', 'D4', 'C4#', '', 'D4', 'E4', 'F4#', 'F4#', '', 'G4', 'A4', 'B4', 'E4', '', '',
    'D5', '', '', 'C5#', '', 'D5', 'B4', 'G4', 'E4', 'F4#', 'G4', 'B3', '', 'G4', 'E4', 'C4#', '', 'D4',
]


class Waveform(Enum):
    Cos = 1
    Sin = 2
    Square = 3
    Sawrooth = 4
    SawroothWidth = 5


def tone(f, t, waveform, fs, width=0.5):
    time = np.linspace(0, t, int(fs * t) + 1)
    x = np.array([])
    cf = 2 * np.pi * f
    if waveform == Waveform.Sin:
        x = np.sin(cf * time)
    elif waveform == Waveform.Cos:
        x = np.cos(cf * time)
    elif waveform == Waveform.Square:
        x = signal.square(cf * time)
    elif waveform == Waveform.Sawrooth:
        x = signal.sawtooth(cf * time)
    elif waveform == Waveform.SawroothWidth:
        x = signal.sawtooth(cf * time, 0.5)
    return x


def musical_tone(f, t, db=-30, fs=44100, waveform=Waveform.Sin):
    x = tone(f, t, waveform, fs)
    i = 2
    while i * f <= 20000:
        x += tone(i * f, t, waveform, fs)
        i += 1
    norm_signal = x / x.max()
    if db == 0:
        return x
    times = 10 ** (db / 20)
    a = times ** (1 / (t * fs))
    time = np.linspace(0, t, int(fs * t) + 1)
    N = time.size
    result_a = np.ones(N)
    for i in range(1, N):
        result_a[i] = result_a[i - 1] * a
    result = norm_signal * result_a
    return result


def create_song(score):
    song = np.zeros(44100)
    for i in score:
        if i == '':
            temp = np.zeros(round(44100 * 0.2))
        else:
            temp = musical_tone(notes[i], float(0.4), db=-30)
        song = np.concatenate((song, temp))
    return song


def create_graphic(t, x):
    plt.xlim(0, 0.001)
    plt.stem(t, x)
    plt.show()


if __name__ == "__main__":
    fs: int = 44100
    f: int = 1000
    waveform: Enum = Waveform.Sin
    t: int = 5
    db = -30
    x: np.float_ = tone(f, t, waveform, fs)
    x2: np.float_ = tone(f + fs, t, waveform, fs)
    time = np.linspace(0, t, int(fs * t) + 1)
    write('example3.wav', fs, x2)
    write('example1.wav', fs, x)
    create_graphic(time, x)
    write('example2.wav', fs, musical_tone(1000, 4, db, fs))
    write("melody.wav", fs, create_song(score_raffaello))

