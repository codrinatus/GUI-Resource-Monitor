import psutil
from datetime import timedelta


# class ResourceMonitor:
def init():
    # cpu
    print("cpu")
    cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
    print(cpu_percent)
    curr_cpu_freq = psutil.cpu_freq(percpu=False)[0]
    max_cpu_freq = psutil.cpu_freq(percpu=False)[2]
    print(curr_cpu_freq)
    print(max_cpu_freq)
    print(psutil.getloadavg())
    print("\n memory")

    # memory
    print(psutil.virtual_memory())
    total_ram = psutil.virtual_memory()[0]
    available_ram = psutil.virtual_memory()[1]
    percent_ram = psutil.virtual_memory()[2]
    used_ram = psutil.virtual_memory()[3]
    print(total_ram)
    print(available_ram)
    print(percent_ram)
    print("\n disk")

    # disk
    paths = []
    disk_total = []
    disk_used = []
    disk_free = []
    disk_percentage = []
    for partitions in psutil.disk_partitions():
        paths.append(partitions[0])
    for i in paths:
        print(psutil.disk_usage(i))
        disk_total.append(psutil.disk_usage(i)[0])
        disk_used.append(psutil.disk_usage(i)[1])
        disk_free.append(psutil.disk_usage(i)[2])
        disk_percentage.append(psutil.disk_usage(i)[3])
    print(disk_total)
    print(disk_used)
    print(disk_free)
    print(disk_percentage)
    print("\n network")

    # network
    print(psutil.net_io_counters(pernic=False, nowrap=True))
    bytes_sent = psutil.net_io_counters(pernic=False, nowrap=True)[0]
    bytes_recv = psutil.net_io_counters(pernic=False, nowrap=True)[1]
    print(psutil.net_if_stats())
    net_dict = psutil.net_if_stats()
    # print(psutil.net_connections(kind='inet'))
    net_filt = {k: v for k, v in net_dict.items() if v[0] is not False}
    print(net_filt)

    print("\n sensors")

    # sensors
    print(psutil.sensors_battery())
    battery_percent = psutil.sensors_battery()[0]
    battery_plugged = psutil.sensors_battery()[2]
    if battery_plugged is False:
        battery_sec_left = timedelta(seconds=psutil.sensors_battery()[1])
    else:
        battery_sec_left = False
    print(battery_percent)
    print(battery_sec_left)
    print(battery_plugged)


init()
