import matplotlib.pyplot as plt
import numpy as np
from sdr_ranging_func import *

data = read_data('3_0m.txt')
mean = mean_clean(data)[0]
print(mean)

# data = np.array([84362.923, 84413.269, 84443.501, 84505.911, 84452.277])
# plt.figure('测距结果呈现')
# plt.plot(['10m', '15m', '20m', '25m', '30m'], data)
# plt.xlabel('Ground-truth')
# plt.ylabel('Number of samples')
# plt.show()
