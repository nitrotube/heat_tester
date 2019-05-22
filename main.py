import subprocess
import datetime
import time
import csv

STAT_INTERVAL = 1

print("The logger will run till stopped. For automated testing see _test.py files.")

date_string = str(datetime.datetime.now().strftime('%d_%m_%y_%H_%M_%S'))
print(date_string)

with open(date_string+'.csv', 'w', newline='') as csvfile:
    my_writer = csv.writer(csvfile, delimiter=',',
                           quotechar='"', quoting=csv.QUOTE_MINIMAL)
    my_writer.writerow(['Zeit', 'Core 0 Temp', 'Core 1 Temp', 'CPU Freq'])
    i = 0
    while True:
        i += 1

        time_string = str(datetime.datetime.now().strftime("%X"))
        print(time_string)

        core0_temp = subprocess.check_output("sensors | grep 'Core 0'", shell=True, universal_newlines=True)
        core0_temp = core0_temp[core0_temp.find('+')+1:core0_temp.find('+')+4]

        if core0_temp[2] == '.':
            core0_temp = core0_temp[:2]
        core0_temp = int(core0_temp)
        print(core0_temp)

        gpu_frequency = subprocess.check_output("sudo cat /sys/class/drm/card0/gt_cur_freq_mhz",
                                                shell=True, universal_newlines=True)
        print(gpu_frequency)

        core1_temp = subprocess.check_output("sensors | grep 'Core 1'", shell=True, universal_newlines=True)
        core1_temp = core1_temp[core1_temp.find('+') + 1:core1_temp.find('+') + 4]

        if core1_temp[2] == '.':
            core1_temp = core1_temp[:2]
        core1_temp = int(core1_temp)
        print(core1_temp)

        cpu_frequency = subprocess.check_output("lscpu | grep 'CPU MHz'", shell=True, universal_newlines=True)
        cpu_frequency = int(cpu_frequency[cpu_frequency.find('.')-4:cpu_frequency.find('.')])
        print(cpu_frequency)

        my_writer.writerow([time_string, core0_temp, core1_temp, cpu_frequency, gpu_frequency])

        time.sleep(STAT_INTERVAL)
