import matplotlib.pyplot as plt
import numpy as np

data = np.array([84362.923, 84413.269, 84443.501, 84505.911, 84452.277])
plt.figure('测距结果呈现')
plt.plot(['10m', '15m', '20m', '25m', '30m'], data)
plt.xlabel('Ground-truth')
plt.ylabel('Number of samples')
plt.show()
