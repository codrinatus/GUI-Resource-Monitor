import os

import psutil
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
import cpuinfo

# cpu

cpu_name = cpuinfo.get_cpu_info()['brand_raw']
cpu_file = open('cpu.txt', "a+")


def cpu_animate():
    """
    Creates a real-time line chart of CPU usage using the matplotlib library. The chart updates every 0.5 seconds.
    :return:launches the animation for the line chart
    """
    fig_cpu = plt.figure()
    ax_cpu = fig_cpu.add_subplot(1, 1, 1)
    cpu_perc = []
    curr_cpu_freq = []
    max_cpu_freq = []
    time = []

    print(datetime.datetime.now().strftime('%d %B %Y'), file=cpu_file)
    print("\n", file=cpu_file)

    ani = animation.FuncAnimation(fig_cpu, cpu, fargs=(time, cpu_perc, curr_cpu_freq, max_cpu_freq, ax_cpu),
                                  interval=500)
    plt.show()


def cpu(i, time, cpu_perc, curr_cpu_freq, max_cpu_freq, ax_cpu):
    """
    Appends the current time, CPU usage, current CPU frequency, and maximum CPU frequency to their respective lists,it
    writes them in the log and plots the CPU usage over time on the chart.
    This function is called every 0.5 seconds by the cpu_animate() function.

    """
    cpu_perc.append(psutil.cpu_percent(interval=0.5, percpu=False))
    curr_cpu_freq.append(psutil.cpu_freq(percpu=False)[0])
    max_cpu_freq.append(psutil.cpu_freq(percpu=False)[2])
    time.append(datetime.datetime.now().strftime('%H:%M:%S'))

    print(str(datetime.datetime.now().strftime('%H:%M:%S')), file=cpu_file)

    print("CPU frequency: ", file=cpu_file)
    print(str(curr_cpu_freq[len(curr_cpu_freq) - 1]), file=cpu_file)

    print("CPU percent: ", file=cpu_file)
    print(str(cpu_perc[len(cpu_perc) - 1]), file=cpu_file)
    print("\n", file=cpu_file)

    time = time[-20:]
    cpu_perc = cpu_perc[-20:]

    ax_cpu.clear()
    ax_cpu.plot(time, cpu_perc)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)


# memory
total_ram = psutil.virtual_memory()[0]
ram_file = open('ram.txt', "a+")


def ram_animate():
    """
    Creates a real-time line chart of RAM usage using the matplotlib library. The chart updates every 1 second.
    :return: launches the animation for the line chart
    """
    fig_ram = plt.figure()
    ax_ram = fig_ram.add_subplot(1, 1, 1)
    available_ram = []
    percent_ram = []
    used_ram = []
    percent_left = []
    time = []

    print(datetime.datetime.now().strftime('%d %B %Y'), file=ram_file)

    ani = animation.FuncAnimation(fig_ram, ram,
                                  fargs=(time, percent_ram, available_ram, percent_left, used_ram, ax_ram),
                                  interval=1000)
    plt.show()


def ram(i, time, percent_ram, available_ram, percent_left, used_ram, ax_ram):
    """
    Appends the current time, percent of used RAM, current available RAM, current used RAM,
    and percent of left RAM to their respective lists,writes them to the respective log file and plots the
    percent of used RAM over time on the chart.
    This function is called every 1 second by the ram_animate() function.
    Parameters:
    i : int (optional,not used)
        current frame number in the animation.
    time: list
        list of the time when the memory usage was logged.
    percent_ram : list
        list of the percent of used ram.
    available_ram : list
        list of the available ram in MB.
    percent_left : list
        list of the percent of left ram.
    used_ram : list
        list of the used ram in MB.
    ax_ram : Axes
        Axes object of the RAM usage chart
    """
    available_ram.append(psutil.virtual_memory()[1] * 0.000001)
    percent_ram.append(psutil.virtual_memory()[2])
    used_ram.append(psutil.virtual_memory()[3] * 0.000001)
    time.append(datetime.datetime.now().strftime('%H:%M:%S'))
    percent_left.append(100 - psutil.virtual_memory()[2])

    print(str(datetime.datetime.now().strftime('%H:%M:%S')), file=ram_file)

    print("Used RAM: ", file=ram_file)
    print(str(used_ram[len(used_ram) - 1]), file=ram_file)

    print("Available RAM: ", file=ram_file)
    print(str(available_ram[len(available_ram) - 1]), file=ram_file)

    print("Used RAM percent: ", file=ram_file)
    print(str(percent_ram[len(percent_ram) - 1]), file=ram_file)

    print("\n", file=ram_file)

    time = time[-20:]
    percent_ram = percent_ram[-20:]

    ax_ram.clear()
    ax_ram.plot(time, percent_ram)
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)


# disk
disk_file = open('disk.txt', "a+")


def disk_animate():
    """
        Creates a real-time line chart of disk usage using the matplotlib library. The chart updates every 1 second.
    :return: launches the animation for the line chart
    """
    paths = []
    disk_total = []
    disk_used = []
    disk_free = []
    disk_percentage = []
    time1 = []
    read_speed = []
    write_speed = []

    print(datetime.datetime.now().strftime('%d %B %Y'), file=disk_file)

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
    """
    Appends the current time, percent of used disk, available disk space, used disk space, read speed and write speed
    to their respective lists,writes them to the respective log file and plots the
    read and write speeds in kilobytes over time on the chart.
    This function is called every 0.5 second by the disk_animate() function.
    :param paths: paths of the mounted disk drives
    """
    print(str(datetime.datetime.now().strftime('%H:%M:%S')), file=disk_file)

    for p in paths:
        disk_total.append(psutil.disk_usage(p)[0] * 0.000001)
        disk_used.append(psutil.disk_usage(p)[1] * 0.000001)
        disk_free.append(psutil.disk_usage(p)[2] * 0.000001)
        disk_percentage.append(psutil.disk_usage(p)[3])
        print("Disk path: ", file=disk_file)
        print(p, file=disk_file)
        print("Used space: ", file=disk_file)
        print(str(disk_used[len(disk_used) - 1]), file=disk_file)
        print("Free space: ", file=disk_file)
        print(str(disk_free[len(disk_free) - 1]), file=disk_file)

    time1.append(datetime.datetime.now().strftime('%H:%M:%S'))

    disk_io_counters = psutil.disk_io_counters(perdisk=False)
    read_speed.append("{:,.2f}".format(disk_io_counters.read_bytes / 1024))
    write_speed.append("{:,.2f}".format(disk_io_counters.write_bytes / 1024))

    print(str(datetime.datetime.now().strftime('%H:%M:%S')), file=disk_file)

    print("Read Speed: ", file=disk_file)
    print(str(read_speed[len(read_speed) - 1]), file=disk_file)

    print("Write Speed: ", file=disk_file)
    print(str(write_speed[len(write_speed) - 1]), file=disk_file)

    print("\n", file=disk_file)

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


# network

network_file = open('network.txt', "a+")


def network_animate():
    """
    Creates a real-time line chart of network usage using the matplotlib library. The chart updates every 1 second.
    :return: launches the animation for the line chart
    """
    bytes_sent = []
    bytes_recv = []
    time = []
    net_dict = psutil.net_if_stats()
    net_filt = {k: v for k, v in net_dict.items() if
                v[0] is not False}  # filters only the network interfaces that are up

    print(datetime.datetime.now().strftime('%d %B %Y'), file=network_file)

    fig_network = plt.figure()
    ax_network = fig_network.add_subplot()
    ani = animation.FuncAnimation(fig_network, network,
                                  fargs=(bytes_sent, bytes_recv, net_filt, time, ax_network), interval=1000)
    plt.show()


def network(i, bytes_sent, bytes_recv, net_filt, time, ax_network):
    """
    Appends the kilobytes sent, kilobytes received,information about the network interfaces that are up and time
    to their respective lists, writes them to the respective log file and plots the kilobytes sent and recieved over time
    on the chart.
    This function is called every 1 second by the network_animate() function.
    :param net_filt: a dictionary with all network interfaces that are up
    """
    bytes_sent.append("{:,.2f}".format(psutil.net_io_counters(pernic=False)[0] / 1024))
    bytes_recv.append("{:,.2f}".format(psutil.net_io_counters(pernic=False)[1] / 1024))
    time.append(datetime.datetime.now().strftime('%H:%M:%S'))

    net_dict = psutil.net_if_stats()
    net_filt = {k: v for k, v in net_dict.items() if
                v[0] is not False}

    print(str(datetime.datetime.now().strftime('%H:%M:%S')), file=network_file)
    for key in net_filt:
        print(key, file=network_file)
        print("Network Speed: ", file=network_file)
        print(net_filt[key][2], file=network_file)
        print("Maximum Transmission Unit:", file=network_file)
        print(net_filt[key][3], file=network_file)
        print('\n', file=network_file)

    print("kb/s received: ", file=network_file)
    print(str(bytes_recv[len(bytes_recv) - 1]), file=network_file)

    print("kb/s sent: ", file=network_file)
    print(str(bytes_sent[len(bytes_sent) - 1]), file=network_file)
    print('\n', file=network_file)

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

# GUI
root = tk.Tk()
root.geometry("640x480")
root.title("GUI Resource Monitor")


def cpuHistory():
    """
    Opens the notepad application and displays the contents of the file 'cpu.txt' which contains the logged CPU usage history.
    """
    cpu = "notepad.exe cpu.txt"
    os.system(cpu)


def cpuWindow():
    """
      Creates a Toplevel window for displaying the current CPU frequency and maximum CPU frequency using the tkinter library.
    Also, it has a button labeled "History" that calls the cpuHistory() function when clicked.
    """
    cpuwindow = tk.Toplevel(root)


    cpuwindow.title("CPU")

    cpuwindow.geometry("640x480")

    tk.Label(cpuwindow, text=cpu_name).pack()
    tk.Label(cpuwindow, text="Current CPU Frequency").pack()
    tk.Label(cpuwindow, text=psutil.cpu_freq(percpu=False)[0]).pack()
    tk.Label(cpuwindow, text="Maximum CPU Frequency").pack()
    tk.Label(cpuwindow,
             text=psutil.cpu_freq(percpu=False)[2]).pack()
    tk.Button(cpuwindow, text="History", command=cpuHistory).pack()
    cpu_animate()


def ramHistory():
    """
        Opens the notepad application and displays the contents of the file 'ram.txt' which contains the logged RAM usage history.

    """
    ram = "notepad.exe ram.txt"
    os.system(ram)


def ramWindow():
    """
     Creates a Toplevel window for displaying the Total ram available,Used ram and Available ram using the tkinter library.
    Also, it has a button labeled "History" that calls the ramHistory() function when clicked.
    """

    ramwindow = tk.Toplevel(root)


    ramwindow.title("RAM")

    ramwindow.geometry("640x480")

    tk.Label(ramwindow, text="Total ram").pack()
    tk.Label(ramwindow, text=total_ram * 0.000001).pack()
    tk.Label(ramwindow, text="Used ram").pack()
    tk.Label(ramwindow, text=psutil.virtual_memory()[3] * 0.000001).pack()
    tk.Label(ramwindow, text="Available ram").pack()
    tk.Label(ramwindow, text=psutil.virtual_memory()[1] * 0.000001).pack()

    tk.Button(ramwindow, text="History", command=ramHistory).pack()
    ram_animate()


def diskHistory():
    """
        Opens the notepad application and displays the contents of the file 'disk.txt' which contains the logged disk usage history.

        """
    disk = "notepad.exe disk.txt"
    os.system(disk)


def diskWindow():
    """
       Creates a Toplevel window for displaying partition info using the tkinter library.
      Also, it has a button labeled "History" that calls the diskHistory() function when clicked.
      """

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

    tk.Button(diskwindow, text="History", command=diskHistory).pack()
    disk_animate()


def networkHistory():
    """
            Opens the notepad application and displays the contents of the file 'disk.txt' which contains the logged disk usage history.

            """
    network = "notepad.exe network.txt"
    os.system(network)


def networkWindow():
    """
         Creates a Toplevel window for displaying network interfaces info using the tkinter library.
        Also, it has a button labeled "History" that calls the diskHistory() function when clicked.
        """
    networkWindow = tk.Toplevel(root)

    networkWindow.title("NETWORK")

    networkWindow.geometry("640x480")

    net_dict = psutil.net_if_stats()
    net_filt = {k: v for k, v in net_dict.items() if
                v[0] is not False}
    for key in net_filt:
        tk.Label(networkWindow, text=key).pack()
        tk.Label(networkWindow, text="Speed:").pack()
        tk.Label(networkWindow, text=net_filt[key][2]).pack()
        tk.Label(networkWindow, text="Maximum Transmission Unit:").pack()
        tk.Label(networkWindow, text=net_filt[key][3]).pack()

    tk.Button(networkWindow, text="History", command=networkHistory).pack()
    network_animate()


tk.Button(root, text="CPU", command=cpuWindow, height=7, width=7).pack(fill=tk.X)
tk.Button(root, text="RAM", command=ramWindow, height=7, width=7).pack(fill=tk.X)
tk.Button(root, text="DISK", command=diskWindow, height=7, width=7).pack(fill=tk.X)
tk.Button(root, text="NETWORK", command=networkWindow, height=7, width=7).pack(fill=tk.X)

root.mainloop()
