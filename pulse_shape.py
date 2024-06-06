import numpy as np

def pulse_shape(data, sps):
  num_taps = 101
  beta = 0.33
  # Assume sample rate is 1 Hz, so sample period is 1, so *symbol* period is 8
  Ts = sps
  t = np.arange(num_taps) - (num_taps-1)//2
  h = np.sinc(t/Ts) * np.cos(np.pi*beta*t/Ts) / (1 - (2*beta*t/Ts)**2)
  data_shaped = np.convolve(data, h)  # pulse shaped
  data_shaped = data_shaped[200:200 + 56]  # only one period
  return data_shaped
