import numpy as np
import matplotlib.pyplot as plt

def diff_code(frame):
    arr = np.array(frame)
    arr = np.where(arr > 0, 1, 0)

    encoded = [arr[0] - arr[-1]]
    for i in range(1, len(arr)):
        diff = np.abs(arr[i] - arr[i-1])
        # diff = np.where(diff == 0, -1, 1)
        diff = int(diff)
        encoded.append(diff)
    return encoded

# frame = [1, 1, 1, -1, -1, 1, -1]  # 7-bit barker code
# frame = diff_code(frame)
# print(frame)

# plt.plot(frame, 'o-')
# plt.show()

def diff_decode(encoded_arr):
    decoded = [encoded_arr[0]]
    for diff in encoded_arr[1:]:
        decoded.append(decoded[-1] + diff)  # 将差值累加到上一个解码值上
    decoded = np.array(decoded)
    decoded = np.where(decoded % 2 == 0, 0, 1)
    return decoded

# decoded_arr = diff_decode(frame)
# print("解码回原始数据:", decoded_arr)
