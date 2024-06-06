import numpy as np
import adi
# import matplotlib.pyplot as plt
from time_rec import *
from norm import *
from pulse_shape import *
import time

start = time.time()
# sample_rate = 1e6  # 1MHz 1M samples per second
# center_freq = 2.4e9  # 2.4GHz
num_samps = 1000  # number of samples per call to rx()

sdr = adi.Pluto("ip:ant.local")

# Construct data
sps = 8  # samples per symbol
frame = [1, 1, 1, -1, -1, 1, -1]  # 7-bit barker code(bpsk)
data = np.array([])

for bit in frame:
    pulse = np.zeros(8)
    pulse[0] = bit  # set the first value to either a 1 or -1, followed by 7 zeros
    data = np.concatenate((data, pulse))  # add the 8 samples to the signal
data = np.tile(data, 20)

# Pulse shaping
data_shaped = pulse_shape(data, sps)

# RX config
sdr.rx_buffer_size = num_samps  # number of received samples

# Transmit data
sdr.tx_cyclic_buffer = True  # enable cyclic buffers
tx_samples = data_shaped*(2**14)
sdr.tx(tx_samples)  # start transmitting

# Receive data
rx_samples = sdr.rx()
rx_samples = normalization(rx_samples)
sdr.tx_destroy_buffer()  # stop transmitting

# Time synchronization
out = time_rec(rx_samples, sps)

result = np.where(out > 0.5, 1, 0)
print(result)

# plt.plot(result[300:400],'.-')
# plt.grid()
# plt.show()
end = time.time()
print(end - start)
