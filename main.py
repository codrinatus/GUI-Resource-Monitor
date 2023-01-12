import psutil
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import tkinter as tk
import cpuinfo

# cpu

cpu_name = cpuinfo.get_cpu_info()['brand_raw']
cpu_file = open('cpu.txt', "a+")


def cpu_animate():
    fig_cpu = plt.figure()
    ax_cpu = fig_cpu.add_subplot(1, 1, 1)
    cpu_perc = []
    curr_cpu_freq = []
    max_cpu_freq = []
    time = []
    ani = animation.FuncAnimation(fig_cpu, cpu, fargs=(time, cpu_perc, curr_cpu_freq, max_cpu_freq, ax_cpu),
                                  interval=500)
    plt.show()


def cpu(i, time, cpu_perc, curr_cpu_freq, max_cpu_freq, ax_cpu):
    cpu_perc.append(psutil.cpu_percent(interval=0.5, percpu=False))
    curr_cpu_freq.append(psutil.cpu_freq(percpu=False)[0])
    max_cpu_freq.append(psutil.cpu_freq(percpu=False)[2])
    time.append(datetime.datetime.now().strftime('%H:%M:%S'))

    time = time[-20:]
    cpu_perc = cpu_perc[-20:]

    ax_cpu.clear()
    ax_cpu.plot(time, cpu_perc)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)


# cpu_animate()

# memory
total_ram = psutil.virtual_memory()[0]
ram_file = open('ram.txt', "a+")


def ram_animate():
    fig_ram = plt.figure()
    ax_ram = fig_ram.add_subplot(1, 1, 1)
    available_ram = []
    percent_ram = []
    used_ram = []
    percent_left = []
    time = []
    ani = animation.FuncAnimation(fig_ram, ram,
                                  fargs=(time, percent_ram, available_ram, percent_left, used_ram, ax_ram),
                                  interval=1000)
    plt.show()


def ram(i, time, percent_ram, available_ram, percent_left, used_ram, ax_ram):
    available_ram.append(psutil.virtual_memory()[1])
    percent_ram.append(psutil.virtual_memory()[2])
    used_ram.append(psutil.virtual_memory()[3])
    time.append(datetime.datetime.now().strftime('%H:%M:%S'))
    percent_left.append(100 - psutil.virtual_memory()[2])

    time = time[-20:]
    percent_ram = percent_ram[-20:]

    ax_ram.clear()
    ax_ram.plot(time, percent_ram)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)


# ram_animate()


# disk
disk_file = open('disk.txt', "a+")


def disk_animate():
    paths = []
    disk_total = []
    disk_used = []
    disk_free = []
    disk_percentage = []
    time1 = []
    read_speed = []
    write_speed = []

    for partitions in psutil.disk_partitions():
        paths.append(partitions[0])
    fig_disk = plt.figure()
    ax_disk = fig_disk.add_subplot()
    ani = animation.FuncAnimation(fig_disk, disk,
                                  fargs=(
                                      time1, paths, disk_total, disk_used, disk_free, disk_percentage, read_speed,
                                      write_speed, ax_disk), interval=500)
    plt.show()


def disk(i, time1, paths, disk_total, disk_used, disk_free, disk_percentage, read_speed, write_speed, ax_disk):
    for p in paths:
        disk_total.append(psutil.disk_usage(p)[0])
        disk_used.append(psutil.disk_usage(p)[1])
        disk_free.append(psutil.disk_usage(p)[2])
        disk_percentage.append(psutil.disk_usage(p)[3])
    time1.append(datetime.datetime.now().strftime('%H:%M:%S'))

    disk_io_counters = psutil.disk_io_counters(perdisk=False)
    read_speed.append("{:,.2f}".format(disk_io_counters.read_bytes / 1024))
    write_speed.append("{:,.2f}".format(disk_io_counters.write_bytes / 1024))

    time1 = time1[-20:]
    read_speed = read_speed[-20:]
    write_speed = write_speed[-20:]

    ax_disk.clear()
    ax_disk.plot(time1, read_speed, '-b', label='read speed')
    ax_disk.plot(time1, write_speed, '-r', label='write speed')
    ax_disk.relim()
    ax_disk.autoscale_view()
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.legend()


# disk_animate()


# network

network_file = open('network.txt', "a+")


def network_animate():
    bytes_sent = []
    bytes_recv = []
    time = []
    net_dict = psutil.net_if_stats()
    net_filt = {k: v for k, v in net_dict.items() if
                v[0] is not False}  # filters only the network interfaces that are up
    fig_network = plt.figure()
    ax_network = fig_network.add_subplot()
    ani = animation.FuncAnimation(fig_network, network,
                                  fargs=(bytes_sent, bytes_recv, net_filt, time, ax_network), interval=1000)
    plt.show()


def network(i, bytes_sent, bytes_recv, net_filt, time, ax_network):
    bytes_sent.append("{:,.2f}".format(psutil.net_io_counters(pernic=False)[0] / 1024))
    bytes_recv.append("{:,.2f}".format(psutil.net_io_counters(pernic=False)[1] / 1024))
    time.append(datetime.datetime.now().strftime('%H:%M:%S'))

    time = time[-20:]
    bytes_sent = bytes_sent[-20:]
    bytes_recv = bytes_recv[-20:]

    ax_network.clear()
    ax_network.plot(time, bytes_recv, '-b', label='kb/s recieved')
    ax_network.plot(time, bytes_sent, '-r', label='kb/s sent')
    ax_network.relim()
    ax_network.autoscale_view()
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.legend()


# network_animate()

# sensors
# print(psutil.sensors_battery())
battery_percent = psutil.sensors_battery()[0]
battery_plugged = psutil.sensors_battery()[2]
if battery_plugged is False:
    battery_sec_left = datetime.timedelta(seconds=psutil.sensors_battery()[1])
else:
    battery_sec_left = False
# print(battery_percent)
# print(battery_sec_left)
# print(battery_plugged)

# GUI
root = tk.Tk()
root.geometry("640x480")
root.title("GUI Resource Monitor")


def cpuWindow():
    # Toplevel object which will
    # be treated as a new window
    cpuwindow = tk.Toplevel(root)

    # sets the title of the
    # Toplevel widget
    cpuwindow.title("CPU")

    # sets the geometry of toplevel
    cpuwindow.geometry("640x480")

    # A Label widget to show in toplevel
    tk.Label(cpuwindow, text=cpu_name).pack()
    tk.Label(cpuwindow, text="Current CPU Frequency").pack()
    tk.Label(cpuwindow, text=psutil.cpu_freq(percpu=False)[0]).pack()
    tk.Label(cpuwindow, text="Maximum CPU Frequency").pack()
    tk.Label(cpuwindow,
             text=psutil.cpu_freq(percpu=False)[2]).pack()
    # tk.Button(cpuwindow,text="History",command=)
    cpu_animate()


def ramWindow():
    # Toplevel object which will
    # be treated as a new window
    ramwindow = tk.Toplevel(root)

    # sets the title of the
    # Toplevel widget
    ramwindow.title("RAM")

    # sets the geometry of toplevel
    ramwindow.geometry("640x480")

    # A Label widget to show in toplevel
    tk.Label(ramwindow, text="Total ram").pack()
    tk.Label(ramwindow, text=total_ram * 0.000001).pack()
    tk.Label(ramwindow, text="Used ram").pack()
    tk.Label(ramwindow, text=psutil.virtual_memory()[3] * 0.000001).pack()
    tk.Label(ramwindow, text="Available ram").pack()
    tk.Label(ramwindow, text=psutil.virtual_memory()[1] * 0.000001).pack()

    # tk.Button(ramwindow,text="History",command=)
    ram_animate()


def diskWindow():
    diskwindow = tk.Toplevel(root)

    diskwindow.title("DISK")

    diskwindow.geometry("640x480")

    paths = []
    for partitions in psutil.disk_partitions():
        paths.append(partitions[0])
    for p in paths:
        tk.Label(diskwindow, text=p).pack()
        disk_total = psutil.disk_usage(p)[0]
        disk_used = psutil.disk_usage(p)[1]
        disk_free = psutil.disk_usage(p)[2]
        tk.Label(diskwindow, text="Total disk capacity").pack()
        tk.Label(diskwindow, text=disk_total * 0.000001).pack()
        tk.Label(diskwindow, text="Used memory").pack()
        tk.Label(diskwindow, text=disk_used * 0.000001).pack()
        tk.Label(diskwindow, text="Free memory").pack()
        tk.Label(diskwindow, text=disk_free * 0.000001).pack()

    # tk.Button(diskwindow,text="History",command=)
    disk_animate()


def networkWindow():
    networkWindow = tk.Toplevel(root)

    networkWindow.title("NETWORK")

    networkWindow.geometry("640x480")

    net_dict = psutil.net_if_stats()
    net_filt = {k: v for k, v in net_dict.items() if
                v[0] is not False}  # filters only the network interfaces that are up
    for key in net_filt:
        tk.Label(networkWindow, text=key).pack()
        tk.Label(networkWindow, text="Speed:").pack()
        tk.Label(networkWindow, text=net_filt[key][2]).pack()
        tk.Label(networkWindow, text="Maximum Transmission Unit:").pack()
        tk.Label(networkWindow, text=net_filt[key][3]).pack()

    # tk.Button(diskwindow,text="History",command=)
    network_animate()


tk.Button(root, text="CPU", command=cpuWindow, height=7, width=7).pack(fill=tk.X)
tk.Button(root, text="RAM", command=ramWindow, height=7, width=7).pack(fill=tk.X)
tk.Button(root, text="DISK", command=diskWindow, height=7, width=7).pack(fill=tk.X)
tk.Button(root, text="NETWORK", command=networkWindow, height=7, width=7).pack(fill=tk.X)
root.mainloop()
