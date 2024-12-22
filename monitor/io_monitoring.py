import time
import psutil
from collections import defaultdict
import matplotlib.pyplot as plt

# 记录开始时间
start_time = time.time()
time_stamps = []
process_io_data = defaultdict(list)

write_io_stat = []
read_io_stat = []
tick = 1
gap_of_tick = 5
while True:
    time_stamps.append(time.time() - start_time)
    wio_sum = 0
    rio_sum = 0
    for proc in psutil.process_iter():
        try:
            io_counters = proc.io_counters()
            process_name = proc.name()
            # 这里使用pyspark启动的进程名为"python3，服务器只运行了一个pyspark任务，所以这里直接统计python3进程的I/O开销"
            if "python3" not in process_name:
                continue
            wio_sum += io_counters.write_bytes
            rio_sum += io_counters.read_bytes
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    write_io_stat.append(wio_sum)
    read_io_stat.append(rio_sum)

    time.sleep(gap_of_tick)
    tick += 1
    # 预计跑5分钟, 5s * 60 = 5分钟
    if tick >=  60:
        break



plt.figure(figsize=(10, 6))

plt.plot(time_stamps, write_io_stat, label='Write I/O', marker='o')
plt.plot(time_stamps, read_io_stat, label='Read I/O', marker='s')

plt.xlabel('时间（秒）')
plt.ylabel('I/O字节数')
plt.title('磁盘读写I/O开销随时间变化趋势')
plt.legend()
plt.grid(True)
plt.show()