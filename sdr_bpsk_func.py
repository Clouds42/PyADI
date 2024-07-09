import numpy as np


def contain(array, sequence):
    seq_len = len(sequence)
    if len(array) < seq_len:
        return False
    for i in range(len(array) - seq_len + 1):
        if np.array_equal(array[i:i+seq_len], sequence):
            return True
    return False


def norm(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


def interp(frame, sps):
    data = np.array([])
    for bit in frame:
        pulse = np.zeros(sps)
        # set the first value to either a 1 or -1, followed by 7 zeros
        pulse[0] = bit
        data = np.concatenate((data, pulse))  # add the 8 samples to the signal
    data = np.tile(data, 20)  # longer for stable wave
    return data


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


def time_rec(rx_samples, sps):
    mu = 0  # initial estimate of phase of sample
    out = np.zeros(len(rx_samples) + 10, dtype=np.complex64)
    # stores values, each iteration we need the previous 2 values plus current value
    out_rail = np.zeros(len(rx_samples) + 10, dtype=np.complex64)
    i_in = 0  # input samples index
    i_out = 2  # output index (let first two outputs be 0)
    while i_out < len(rx_samples) and i_in+16 < len(rx_samples):
        # grab what we think is the "best" sample
        out[i_out] = rx_samples[i_in + int(mu)]
        out_rail[i_out] = int(np.real(out[i_out]) > 0) + \
            1j*int(np.imag(out[i_out]) > 0)
        x = (out_rail[i_out] - out_rail[i_out-2]) * np.conj(out[i_out-1])
        y = (out[i_out] - out[i_out-2]) * np.conj(out_rail[i_out-1])
        mm_val = np.real(y - x)
        mu += sps + 0.3*mm_val
        # round down to nearest int since we are using it as an index
        i_in += int(np.floor(mu))
        mu = mu - np.floor(mu)  # remove the integer part of mu
        i_out += 1  # increment output index
    # remove the first two, and anything after i_out (that was never filled out)
    out = out[2:i_out]
    return out
