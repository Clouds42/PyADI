import threading
import time
import numpy as np
import adi
import matplotlib.pyplot as plt
import queue
from sdr_func import *

# 1.7GHz和2GHz频段时域干扰较小
sdr = adi.Pluto("usb:1.8.5")
sdr.sample_rate = 1000000
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 70
sdr.rx_buffer_size = 100000
sdr.rx_lo = 1750000000
sdr.rx_rf_bandwidth = 20000000
sdr.tx_rf_bandwidth = 20000000
sdr.tx_lo = 1700000000
sdr.tx_hardwaregain_chan0 = 0
# sdr.tx_cyclic_buffer = True
# print(sdr)
data = np.array(np.ones(10))
tx_samples = data*(2**14)


def tx():
    sdr.tx(tx_samples)  # start transmitting
    # sdr.tx_destroy_buffer()
    # return


def rx(q):
    rx_samples = sdr.rx()
    index = find_frame(rx_samples)
    q.put(index)
    # plt.plot(rx_samples)
    # plt.ylim([-2000, 2000])
    # plt.show()


def main():
    start_time = time.time()
    results_queue = queue.Queue()

    i = 0
    epoch = 100
    result = np.zeros(epoch)
    while i < epoch:
        # time.sleep(0.02)
        t1 = threading.Thread(target=tx)
        t2 = threading.Thread(target=rx, args=(results_queue,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        while not results_queue.empty():
            index = results_queue.get()
            print(f"The {i}-th frame detected. Index: {index}")
            result[i] = index

        i = i + 1

    print(result)
    mean = np.mean(result)
    print(mean)
    end_time = time.time()
    print(end_time - start_time)
    plt.plot(result, 'o-')
    plt.grid()
    plt.ylim([0, 70000])
    plt.show()


if __name__ == "__main__":
    main()
