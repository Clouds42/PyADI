import threading
import time
import numpy as np
import adi
import matplotlib.pyplot as plt
import queue
from sdr_ranging_func import *


sdr = adi.Pluto("ip:ant.local")
sdr.sample_rate = 1000000
sdr.rx_rf_bandwidth = 20000000
sdr.tx_rf_bandwidth = 20000000
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 64
sdr.tx_hardwaregain_chan0 = 0
frame = np.array([1, 1, 1, -1, -1, 1, -1])  # 7-bit barker code
data = np.tile(frame, 10)
tx_samples = data * (2**14)

self = 1  # 1 for autonomous sending and receiving and 0 for bidirectional communication
test = 0  # 1 for single and 0 for multible(1 for save data to files)
verbose = 1  # 1 for detailed log output
step = 1
dist = 50  # distance in the filename

sdr.rx_lo = 2400000000 if self else 2500000000
sdr.rx_buffer_size = 4000 if self else 100000

sdr.tx_lo = 2400000000

epoch = 1 if test else 500


def tx():
    sdr.tx(tx_samples)


def rx(q):
    rx_samples = sdr.rx()
    q.put(rx_samples)


def main():
    start_time = time.time()

    i = 0  # current iteration
    j = 0  # control the step
    result = np.zeros(epoch)  # preallocate
    results_queue = queue.Queue()  # bring the result back to the main thread

    while i < epoch:
        t1 = threading.Thread(target=tx)
        t2 = threading.Thread(target=rx, args=(results_queue,))

        t1.start()
        t2.start()

        t1.join()  # wait until the thread terminates
        t2.join()

        rx_samples = results_queue.get()
        rx_samples_real = np.real(rx_samples)  # convert complex to real
        # binarization for correlate
        rx_samples_bin = binarize(rx_samples_real)

        correlation = np.correlate(rx_samples_bin, frame, mode='full')
        index = find_frame(correlation, 0, 0 if self else 50000)

        if test:
            break

        if verbose:
            if j > step - 1:
                print(f'\rThe {i}-th frame detected. Index: {index}', end='')
                j = 1
            else:
                j = j + 1

        result[i] = index

        i = i + 1

    if test:
        print(f'Result: {index}')
    else:
        mean = np.round(mean_clean(result)[0], 4)
        print(f'\rMean: {mean} (exclude the outliers with 3-order)')

        current_time = time.localtime()
        formatted_time = time.strftime('%m%d%H%M%S', current_time)
        filename = f'./data/{dist}m_{formatted_time}_{mean}.txt'
        save_data(result, filename)

    end_time = time.time()
    print(f'\nTime spent: {end_time - start_time} s')

    if test:
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
        plt.ylim([0, sdr.rx_buffer_size])

        result_clean = mean_clean(result)[1]
        plt.subplot(2, 1, 2)
        plt.title('Result - clean(3-order)')
        plt.plot(result_clean, 'go-')
        plt.xlim([0, epoch])
        plt.ylim([0, sdr.rx_buffer_size])

        plt.show()


if __name__ == "__main__":
    main()
