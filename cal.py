import numpy as np
import matplotlib.pyplot as plt
from sdr_ranging_func import *

data = read_data('./data/40m.txt')
data = data[data > 80000]
print(mean_clean(data)[0])
