from sdr_ranging_func import *
import matplotlib.pyplot as plt
import numpy as np


data = read_data('2_25m.txt')
plt.subplot(5, 1, 1)
plt.plot(data, 'go-')
plt.ylim([0, 90000])
plt.xlim([0, 1500])
print(np.mean(data))

data = remove_outliers(data)
plt.subplot(5, 1, 2)
plt.plot(data, 'go-')
plt.ylim([0, 90000])
plt.xlim([0, 1500])
print(np.mean(data))

data = remove_outliers(data)
plt.subplot(5, 1, 3)
plt.plot(data, 'go-')
plt.ylim([0, 90000])
plt.xlim([0, 1500])
print(np.mean(data))

data = remove_outliers(data)
plt.subplot(5, 1, 4)
plt.plot(data, 'go-')
plt.ylim([0, 90000])
plt.xlim([0, 1500])
print(np.mean(data))

data = remove_outliers(data)
plt.subplot(5, 1, 5)
plt.plot(data, 'go-')
plt.ylim([0, 90000])
plt.xlim([0, 1500])
print(np.mean(data))

plt.show()
