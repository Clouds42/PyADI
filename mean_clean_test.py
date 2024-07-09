from sdr_ranging_func import *
import matplotlib.pyplot as plt
import numpy as np


data = read_data('2_25m.txt')
plt.subplot(5, 1, 1)
plt.plot(data, 'go-')
plt.ylim([0, 90000])
plt.xlim([0, 1500])
print(np.mean(data))

data_ro1 = remove_outliers(data)
plt.subplot(5, 1, 2)
plt.plot(data_ro1, 'go-')
plt.ylim([0, 90000])
plt.xlim([0, 1500])
print(np.mean(data_ro1))

data_ml1 = mean_clean(data, 1)
plt.subplot(5, 1, 3)
plt.plot(data_ml1, 'go-')
plt.ylim([0, 90000])
plt.xlim([0, 1500])
print(np.mean(data_ml1))

data_ro2 = remove_outliers(data_ro1)
plt.subplot(5, 1, 4)
plt.plot(data_ro2, 'go-')
plt.ylim([0, 90000])
plt.xlim([0, 1500])
print(np.mean(data_ro2))

data_ml2 = mean_clean(data, 2)
plt.subplot(5, 1, 5)
plt.plot(data_ml2, 'go-')
plt.ylim([0, 90000])
plt.xlim([0, 1500])
print(np.mean(data_ml2))

plt.show()
