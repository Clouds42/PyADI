import threading
import time
import numpy as np
import adi
import matplotlib.pyplot as plt
import queue
from sdr_func import *

local = 1  # 1 or 0
single = 0  # 1 or 0
plot = 0

sdr = adi.Pluto("ip:ant.local")
sdr.sample_rate = 1000000

sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_lo = 2400000000 if local == 1 else 915000000
sdr.rx_rf_bandwidth = 20000000
sdr.rx_hardwaregain_chan0 = 64
sdr.rx_buffer_size = 4000

sdr.tx_lo = 2400000000
sdr.tx_rf_bandwidth = 20000000
sdr.tx_hardwaregain_chan0 = 0
# sdr.tx_cyclic_buffer = True

epoch = 1 if single == 1 else 100
start_index = 0 if local == 1 else 40000

frame = np.array([1, 1, 1, -1, -1, 1, -1])
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
        threhold = np.mean([0, np.max(rx_samples_real)])

        rx_samples_dec = np.where(rx_samples_real > threhold, 1,
                                  np.where(rx_samples_real < np.negative(threhold), -1, 0))

        correlation = np.correlate(rx_samples_dec, frame, mode='full')
        index = find_frame(correlation, 0, 0)
        print(f"The {i}-th frame detected. Index: {index}")
        result[i] = index

        i = i + 1

    print(result)
    if single == 0:
        mean = np.mean(result[1:])
        print(mean)

    end_time = time.time()
    print(end_time - start_time)

    if plot == 1:
        plt.figure("Result")
        plt.grid()

        plt.subplot(3, 1, 1)
        plt.title("Received")
        plt.plot(rx_samples_real)
        plt.ylim([-2048, 2048])

        plt.subplot(3, 1, 2)
        plt.title("Decoded")
        plt.plot(rx_samples_dec, 'go-')

        plt.subplot(3, 1, 3)
        plt.title("Correlated")
        plt.plot(correlation, 'go-')

        plt.show()
    else:
        plt.plot(result, 'o-')
        plt.grid()
        plt.ylim([0, 4000])
        plt.show()


if __name__ == "__main__":
    main()
