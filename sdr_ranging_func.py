import numpy as np
import re


def binarize(data):
    threshold = np.mean([0, np.max(data)])
    data_bin = np.where(data > threshold, 1, np.where(
        data < np.negative(threshold), -1, 0))
    return data_bin


def find_frame(array, threhold=0, start_index=50000):
    sliced_array = array[start_index:]
    abs_array = np.abs(sliced_array)
    greater_than = abs_array > threhold
    index = np.argmax(greater_than)
    result = index + start_index
    return result


def remove_outliers(data):
    threshold = 3
    mean = np.mean(data)
    std = np.std(data)
    z_scores = [(x - mean) / std for x in data]
    filtered_data = [x for x, z in zip(data, z_scores) if abs(z) < threshold]
    return filtered_data


def mean_clean(data, order=3):
    clean_data = remove_outliers(data)
    while order > 1:
        clean_data = remove_outliers(clean_data)
        order = order - 1

    return np.array([np.mean(clean_data), clean_data], dtype=object)


def read_data(filename):
    with open(filename, 'r') as file:
        data = file.read()
    cleaned_data = re.findall(r'\d+\.\d+|\d+', data)
    return np.array(cleaned_data, dtype=np.float64)


def save_data(data, filename):
    with open(filename, 'w') as file:
        file.write(str(data))
