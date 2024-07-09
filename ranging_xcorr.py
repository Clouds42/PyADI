import threading
import time
import numpy as np
import adi
import matplotlib.pyplot as plt
import queue
from sdr_ranging_func import *

filename = '3_0m.txt'

self = 1  # 1 or 0
test = 0  # 1 or 0
verbose = 1
step = 25

sdr = adi.Pluto("ip:ant.local")
sdr.sample_rate = 1000000
sdr.rx_rf_bandwidth = 20000000
sdr.tx_rf_bandwidth = 20000000

sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 64
sdr.tx_hardwaregain_chan0 = 0

sdr.rx_lo = 2400000000 if self == 1 else 2500000000
sdr.rx_buffer_size = 4000 if self == 1 else 100000

sdr.tx_lo = 2400000000
# sdr.tx_cyclic_buffer = True

epoch = 1 if test == 1 else 500

frame = np.array([1, 1, 1, -1, -1, 1, -1])  # 7-bit barker code
data = np.tile(frame, 10)
tx_samples = data * (2**14)


def tx():
    sdr.tx(tx_samples)


def rx(q):
    rx_samples = sdr.rx()
    q.put(rx_samples)


def main():
    start_time = time.time()

    i = 0
    j = 0
    result = np.zeros(epoch)
    results_queue = queue.Queue()

    while i < epoch:
        t1 = threading.Thread(target=tx)
        t2 = threading.Thread(target=rx, args=(results_queue,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        rx_samples = results_queue.get()
        rx_samples_real = np.real(rx_samples)
        rx_samples_bin = binarize(rx_samples_real)

        correlation = np.correlate(rx_samples_bin, frame, mode='full')
        index = find_frame(correlation, 0, 0 if self == 1 else 50000)

        if test == 1:
            break

        if verbose:
            if j > step - 1:
                print(f"The {i}-th frame detected. Index: {index}")
                j = 1
            else:
                j = j + 1

        result[i] = index

        i = i + 1

    if test == 1:
        print(f'Result: {index}')
    else:
        # print(f'\nResult:\n{result}')
        mean = mean_clean(result)[0]
        print(f'\nMean: {mean} (exclude the outliers)')

    end_time = time.time()
    print(f'\nTime spent: {end_time - start_time} s')

    save_to_file(result, filename)

    if test == 1:
        plt.figure("Result")
        plt.grid()

        plt.subplot(3, 1, 1)
        plt.title("Received")
        plt.plot(rx_samples_real)
        plt.ylim([-2048, 2048])

        plt.subplot(3, 1, 2)
        plt.title("Binarization")
        plt.plot(rx_samples_bin, 'go-')

        plt.subplot(3, 1, 3)
        plt.title("Correlated")
        plt.plot(correlation, 'go-')

        plt.show()
    else:
        plt.figure("Result")
        plt.grid()

        plt.subplot(2, 1, 1)
        plt.title('Result - raw')
        plt.plot(result, 'go-')
        plt.xlim([0, epoch])
        plt.ylim([0, 4000 if self == 1 else 90000])

        result_clean = mean_clean(result)[1]
        plt.subplot(2, 1, 2)
        plt.title('Result - clean')
        plt.plot(result_clean, 'go-')
        plt.xlim([0, epoch])
        plt.ylim([0, 4000 if self == 1 else 90000])

        plt.show()


if __name__ == "__main__":
    main()
