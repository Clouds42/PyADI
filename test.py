import adi
import time

time_start = time.time()

sdr = adi.Pluto("ip:ant.local")
print(sdr)
sdr.rx_buffer_size = 10
data = sdr.rx()
print(data)

time_end = time.time()
print('Time cost',time_end-time_start,'s')
