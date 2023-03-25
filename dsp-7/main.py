import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf


def create_signal(msg):
    res = np.zeros(1000)
    dot = np.ones(20)
    dash = np.ones(60)
    space_word = np.zeros(120)
    space_char = np.zeros(40)
    empty = np.zeros(20)

    for c in msg:
        if c == '.':
            res = np.concatenate((res, dot, empty))
        elif c == '-':
            res = np.concatenate((res, dash, empty))
        elif c == ' ':
            res = np.concatenate((res, space_char))
        elif c == '/':
            res = np.concatenate((res, space_word))
        else:
            raise Exception()
    return res


def mse(lhs, rhs):
    result = np.array([(lhs[i]-rhs[i])**2 for i in range(len(lhs))])
    return np.mean(result)


def main():
    msg = ".-/- .-. . ./.. .../-.- -. --- .-- -./-... -.--/.. - .../..-. .-. ..- .. -"
    clear_signal = create_signal(msg)
    print(clear_signal.shape)
    plt.figure('Reference', figsize=(20, 1))
    plt.plot(clear_signal)
    first_res = np.load('13f.npy')
    plt.figure('BandpassReconstructed', figsize=(20, 1))
    plt.plot(first_res)
    print(first_res.shape)
    m = 21
    shift = int(m/2)
    first_res = np.concatenate((first_res[shift:], np.zeros(shift)))
    print('6 lab: ', mse(clear_signal, first_res))
    signal = np.load('13.npy')
    plt.figure('Input', figsize=(20, 1))
    plt.plot(signal)

    # 3.1
    r_y = acf(signal[1000:], adjusted=True, nlags=m)*np.var(signal[1000:])
    d = np.var(signal[:1000])
    r_xy = r_y.copy()
    r_xy[0] -= d

    # 3.2
    A = np.fromfunction(lambda i, j: r_y[np.abs(i.astype(int)-j.astype(int))], (len(r_y), len(r_y)), dtype=float)
    b = np.array([r_xy[np.abs(i-shift)] for i in range(len(r_xy))])

    # 3.3
    h = np.linalg.solve(A, b)
    # plt.figure('h')
    # plt.plot(h)
    # 4
    result = sp.signal.convolve(signal, h)
    result = np.concatenate((result[shift:], np.zeros(shift)))
    # 5
    print('7 lab: ', mse(clear_signal, result))
    plt.figure('SuboptimalReconstructed', figsize=(20, 1))
    plt.plot(result)
    plt.show()


if __name__ == '__main__':
    main()
