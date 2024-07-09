import numpy as np
import adi
import matplotlib.pyplot as plt
from bpsk.sdr_bpsk_func import *
import time

start = time.time()

# sample_rate = 1e6  # bandwidth 1MHz / 1M samples per second
# center_freq = 2.4e9  # 2.4GHz
num_samps = 700  # number of samples per call to rx()

# Connect to Pluto SDR
sdr = adi.Pluto("ip:ant.local")

# RX config
sdr.rx_buffer_size = num_samps  # number of received samples

# Construct data
sps = 8  # samples per symbol
frame = [1, 1, 1, -1, -1, 1, -1]  # 7-bit barker code(bpsk)

# Data interpolation
data = interp(frame, sps)

# Pulse shaping
data_shaped = pulse_shape(data, sps)

# Transmit data
sdr.tx_cyclic_buffer = True  # enable cyclic buffers
# Pluto SDR accepts value between -2^14 to 2^14
tx_samples = data_shaped*(2**14)
sdr.tx(tx_samples)  # start transmitting

# Receive data
rx_samples = sdr.rx()  # receiving
rx_samples = norm(rx_samples)  # normalizing to (0, 1)
# plt.plot(np.real(rx_samples), np.imag(rx_samples), '.')
# plt.xlim((-0.1, 1.1))
# plt.ylim((-1.1, 1.1))
# plt.show()
sdr.tx_destroy_buffer()  # stop transmitting

# Time synchronization
out = time_rec(rx_samples, sps)

# BPSK demodulation
result = np.where(out > 0.5, 1, 0)
print(result)

# Received the frame that had just transmitted
print(contain(result, [1, 1, 1, 0, 0, 1, 0]) |
      contain(result, [1, 1, 1, 0, 1, 1, 0]) |
      contain(result, [1, 1, 1, 1, 0, 1, 0]))

end = time.time()
print(end - start)
