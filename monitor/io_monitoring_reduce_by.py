import time
import psutil
import signal
from collections import defaultdict
import matplotlib.pyplot as plt

# 记录开始时间
start_time = time.time()
time_stamps = []
process_io_data = defaultdict(list)

write_io_stat = []
read_io_stat = []
tick = 1
gap_of_tick = 2
second = 0.5
assert gap_of_tick * second == 1
start_wio_sum = 0
start_rio_sum = 0
for proc in psutil.process_iter():
    try:
        io_counters = proc.io_counters()
        process_name = proc.name()
        if "java" not in process_name:
            continue
        start_wio_sum += io_counters.write_bytes
        start_rio_sum += io_counters.read_bytes

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        continue

stop =  0

def signal_handler(sig, frame):
    global stop
    stop = 1

while stop == 0:
    time_stamps.append(tick * gap_of_tick)
    wio_sum = 0
    rio_sum = 0
    for proc in psutil.process_iter():
        try:
            io_counters = proc.io_counters()
            process_name = proc.name()
            if "java" not in process_name:
                continue
            wio_sum += io_counters.write_bytes
            rio_sum += io_counters.read_bytes
            # 清空

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    prev_wio_sum = wio_sum
    prev_rio_sum = rio_sum

    wio_sum -= start_wio_sum
    rio_sum -= start_rio_sum

    start_rio_sum = prev_rio_sum
    start_wio_sum = prev_wio_sum

    write_io_stat.append(wio_sum)
    read_io_stat.append(rio_sum)

    print(f"tick: {tick}, write_io: {wio_sum}, read_io: {rio_sum}")

    time.sleep(gap_of_tick)
    tick += 1
    signal.signal(signal.SIGINT, signal_handler)

    # 预计跑5分钟, 5s * 60 = 5分钟
    if tick >= 3 * 60 * second + 30:
        break

# 写入到experiment/groupByKey/io_stat.txt,写入三行数据， 分别是时间戳，写I/O，读I/O
# with open("experiment_data/groupByKey/io_stat_2_second.csv", "w") as f:
with open("experiment_data/reduceByKey/io_stat_uniform.csv", "w") as f:
    f.write("time_stamp,write_io,read_io\n")
    for i in range(len(time_stamps)):
        f.write(f"{time_stamps[i]},{write_io_stat[i]},{read_io_stat[i]}\n")


plt.figure(figsize=(10, 6))

plt.plot(time_stamps, write_io_stat, label='Write I/O', marker='o')
plt.plot(time_stamps, read_io_stat, label='Read I/O', marker='s')

plt.xlabel('time (S)')
plt.ylabel('I/O bytes')
plt.title('I/O')
plt.legend()
# plt.savefig("experiment_data/groupByKey/io_stat_ten_second.png")
plt.savefig("experiment_data/reduceByKey/io_stat_uniform.png")
plt.grid(True)
plt.show()
