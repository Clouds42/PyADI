import time

i = 0
while i < 10:
    print(f'\r{i}', end='')
    i = i + 1
    time.sleep(0.5)
