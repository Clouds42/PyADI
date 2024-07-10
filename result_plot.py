import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


files = [f for f in os.listdir('./data/') if f.endswith('.txt')]

data = []
for file in files:
    parts = file.split('_')
    distance = parts[0]
    timestamp = parts[1]
    num_samples = float(parts[2].replace('.txt', ''))

    data.append({'Distance': distance, 'Data': num_samples})


df = pd.DataFrame(data)
result = df.groupby('Distance')['Data'].mean().reset_index()
print(result)

plt.figure('测距结果呈现')
plt.plot(np.array(result['Distance']), np.array(result['Data']), 'go-')
plt.xlabel('Ground-truth')
plt.ylabel('Number of samples')
plt.show()
