import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages
import glob
import numpy as np
from datetime import datetime
import config
from matplotlib.patches import Ellipse, Circle

# To get rid of memory warnings
plt.rcParams.update({'figure.max_open_warning': 0})


class FoundFiles:
    def __init__(self, path, creation_time):
        self.path = path
        self.creation_time = datetime.strptime(creation_time, "%d_%m_%y_%H_%M_%S")


# Location of the folder with CSV files
files_array = glob.glob(config.CSV_FOLDER_LOCATION + '*.csv')
files_sorted = []

for file in files_array:
    files_sorted.append(FoundFiles(file, file[53:70]))

files_sorted.sort(key=lambda x: x.creation_time)

print('Files in folder: ')
print(len(files_sorted))


def add_titlebox(ax, text):
    ax.text(.5, .08, text,
            horizontalalignment='center',
            transform=ax.transAxes,
            bbox=dict(facecolor='white', alpha=0.6),
            fontsize=14)
    return ax


with open('results.csv', 'w') as results_file:
    pp = PdfPages('full_report.pdf')
    cp = PdfPages('critical.pdf')
    my_writer = csv.writer(results_file, delimiter=',',
                           quotechar='"', quoting=csv.QUOTE_MINIMAL)
    i = 0
    for file in files_sorted:
        i += 1
        print(str(i) + '. ' + file.path)
        file_path = file.path
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            x = []
            core1_temp = []
            core2_temp = []
            cpu_freq = []
            gpu_freq = []
            critical = False
            try:
                for line in csv_reader:
                    if line_count > 10:
                        x.append(line[0])
                        core1_temp.append(int(line[1]))
                        core2_temp.append(int(line[2]))
                        cpu_freq.append(int(line[3]))
                        gpu_freq.append(int(line[4]))
                        if (int(line[1]) > config.CRITICAL_CPU_TEMP) or (int(line[2]) > config.CRITICAL_CPU_TEMP) or\
                                (int(line[3]) < config.CRITICAL_CPU_FREQ):
                            critical = True
                    line_count += 1
            except:
                pass

            if line_count >= config.MINIMAL_LINE_NUMBER:
                print("Length: " + str(len(x)))

                cpu_temp_limit = [config.CRITICAL_CPU_TEMP for i in range(len(x))]
                cpu_freq_limit = [config.CRITICAL_CPU_FREQ for i in range(len(x))]

                gridsize = (3, 2)
                fig = plt.figure(figsize=(12, 8))

                ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=2, rowspan=2)
                ax2 = plt.subplot2grid(gridsize, (2, 0))
                ax3 = plt.subplot2grid(gridsize, (2, 1))

                ax1.plot(x, cpu_freq)
                ax1.plot(cpu_freq_limit, 'm--')

                ax2.plot(x, core1_temp)
                ax2.plot(x, core2_temp)
                ax2.plot(x, cpu_temp_limit, 'm--')

                ax3.plot(x, gpu_freq)

                plt.sca(ax1)
                add_titlebox(ax1, "CPU Frequency")
                ax1.set_title(file_path[53:61] + "   " + file_path[62:70])
                plt.grid()
                plt.yticks(np.arange(1500, 4100, 100))
                ax1.xaxis.set_major_locator(ticker.MultipleLocator(len(x) / 12.5))

                plt.sca(ax2)
                add_titlebox(ax2, "CPU Temperature")
                plt.grid()
                plt.yticks(np.arange(30, 110, 5))
                ax2.xaxis.set_major_locator(ticker.MultipleLocator(len(x) / 5.5))

                plt.sca(ax3)
                add_titlebox(ax3, "GPU Frequency")
                plt.grid()
                plt.yticks(np.arange(100, 1100, 100))
                ax3.xaxis.set_major_locator(ticker.MultipleLocator(len(x) / 5.5))

                # Add red circles on CPU Frequency plot
                for counter in range(1, len(cpu_freq) - 1):
                    if cpu_freq[counter] < config.CRITICAL_CPU_FREQ and cpu_freq[counter] < cpu_freq[counter - 1] and cpu_freq[counter] < cpu_freq[counter + 1]:
                        circle = Ellipse((x[counter], cpu_freq[counter]), len(x)/120, 40, color='r')
                        ax1.add_artist(circle)

                # Add red circles on CPU Temperature plot
                for counter in range(1, len(core1_temp) - 1):
                    if core1_temp[counter] > config.CRITICAL_CPU_TEMP and core1_temp[counter] > core1_temp[counter - 1] and core1_temp[counter] > core1_temp[counter + 1]:
                        circle = Ellipse((x[counter], core1_temp[counter]), len(x)/200, 6, color='r')
                        ax2.add_artist(circle)
                    if core2_temp[counter] > config.CRITICAL_CPU_TEMP and core2_temp[counter] > core2_temp[counter - 1] and core2_temp[counter] > core2_temp[counter + 1]:
                        circle = Ellipse((x[counter], core2_temp[counter]), len(x)/200, 6, color='r')
                        ax2.add_artist(circle)

                #plt.show()
                pp.savefig(fig)

                if critical:
                    cp.savefig(fig)
            else:
                print("The number of lines does not reach the minimum limit")
    pp.close()
    cp.close()
