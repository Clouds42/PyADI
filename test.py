import time

# 获取当前时间的结构化时间（struct_time）
current_time = time.localtime()

# 格式化时间为 YYMMDDhhmmss
formatted_time = time.strftime('%y%m%d%H%M%S', current_time)

print(formatted_time)
