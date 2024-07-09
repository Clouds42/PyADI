import adi
import time
import matplotlib.pyplot as plt

time_start = time.time()

sdr = adi.Pluto("ip:ant.local")
sdr.sample_rate = 1000000
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 64
sdr.rx_buffer_size = 100000
sdr.rx_lo = 2500000000
sdr.rx_rf_bandwidth = 20000000
data = sdr.rx()

time_end = time.time()
print('Time cost',time_end-time_start,'s')

plt.plot(data)
plt.ylim([-2048, 2048])
plt.show()
