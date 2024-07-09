import re
import numpy as np
import matplotlib.pyplot as plt


def clean_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    # Remove non-numeric characters and split by whitespace
    cleaned_data = re.findall(r'\d+\.\d+|\d+', data)
    return np.array(cleaned_data, dtype=np.float64)


def remove_outliers(data, threshold = 3):
    mean = np.mean(data)
    std = np.std(data)
    z_scores = [(x - mean) / std for x in data]
    filtered_data = [x for x, z in zip(data, z_scores) if abs(z) < threshold]
    # return np.mean(filtered_data)
    return filtered_data


# Clean and load data
data = clean_data('2_10m.txt')

# Remove outliers and compute mean
plt.subplot(3, 1, 1)
plt.plot(data, 'go-')
plt.xlim([0, 1500])
plt.ylim([0, 90000])
filtered_data = remove_outliers(data)
plt.subplot(3, 1, 2)
plt.plot(filtered_data, 'go-')
plt.xlim([0, 1500])
plt.ylim([0, 90000])
filtered_data = remove_outliers(filtered_data)
filtered_data = remove_outliers(filtered_data)
plt.subplot(3, 1, 3)
plt.plot(filtered_data, 'go-')
plt.xlim([0, 1500])
plt.ylim([0, 90000])
plt.show()

print(np.mean(filtered_data))
