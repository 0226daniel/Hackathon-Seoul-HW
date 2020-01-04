import sys
import matplotlib.pyplot as plt

import numpy as np
import scipy
from scipy.io import wavfile


if __name__ == "__main__":
    me, name, *args = sys.argv

    fs, data = wavfile.read(name)

    a = data.T[0]
    b = a / fs
    c = np.fft.fft(b) / len(b)
    d = len(c) // 2

    print("Frequency Rate", fs)

    plt.subplot(2, 1, 1)
    plt.plot(data / len(data), 'b')

    #################################
    hearable = abs(c[:20000])

    calibrated = sorted(c)[1000:19000]
    mean = sum(calibrated) / 18000
    print(mean)

    plt.subplot(2, 1, 2)
    plt.plot(hearable, 'r')
    plt.plot([mean for x in range(20000)], 'g')
    plt.show()

    """plt.plot(abs(c[:20000]), 'r')
    plt.show()"""
