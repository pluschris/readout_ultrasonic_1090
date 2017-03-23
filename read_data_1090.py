#!/usr/bin/python3
# ##########################################################################
# info: This script fetches the screen-data from Karl Deutsch Echograph 1090
#
# date: 2017-03-23
# version: 0.2.1
# author: pluschris
#
# history:  V0.2: cleanup code
#           V0.1: First version
#
# ##########################################################################
# Import solution :-)

import serial
import numpy
import csv
import time
import os
import sys
import matplotlib.pyplot as plt

# ##########################################################################
# config:

SERIAL_PORT = "/dev/ttyUSB0"
FILE_NAME = "file_name"

############################################################################
def read_device(dev):
    data=b''
    read_data = True
    while read_data:
        data+=dev.read()
        if dev.inWaiting() == 0:
            time.sleep(0.1)
            if dev.inWaiting() == 0:
                read_data = False
    return data
############################################################################
#Start Measurement:

print('Opening Device...')
dev = serial.Serial(SERIAL_PORT,57600)

# send commands to init measurement:
command_read_amplitude=b'\x02AG\x03'
dev.write(command_read_amplitude)

############################################################################
# read data, select the right bytes for screen data:

data=read_device(dev)[6576:-24]

############################################################################
# convert bits to something readable:

i=0
x=1
x_list=[]
y_list=[]
while i<len(data):
    #maximum value is 0xE0=224 when Amplitude is 0, min value is 0 when Amplitude is 100%:
    #First Byte is difference to second byte, second byte is fix value:
    #Devices sends HEX as ASCII
    diff = int(data[i:i+2], 16)
    fix=224-int(data[i+2:i+4], 16)
    diff=fix-diff

    #let's scale to 10 divisions
    fix=float(fix)/224*10
    diff=float(diff)/224*10

    x_list.append(x)
    x_list.append(x)
    if i>0:
        #calc in which order we have to add the points to get a smooth drawing:
        if y_list[-1] <= fix and y_list[-1] <= diff:
            y_list.append(diff)             # small value first: diff is always smaller than fix
            y_list.append(fix)
        else:
            y_list.append(fix)              #large value first
            y_list.append(diff)
    else:
        y_list.append(diff)
        y_list.append(fix)

    x+=1
    i+=4

    #we just need the grid-area of the screen: 10 divisions is x=350 so let's cut off:
    if x>350:
        break
    
#scale x-axis to 10 divisions:
x_list=[float(i)/350*10 for i in x_list]

############################################################################
#plot/print:

print(y_list)
plt.figure(figsize=(10,5))
plt.gcf().patch.set_facecolor('white')
plt.plot(x_list, y_list,  ls='-',  marker=None,color='darkcyan')
plt.xlim(0,10)
plt.ylim(0,10)
plt.xticks(numpy.arange(0,11,1))
plt.gcf().axes[0].yaxis.grid(True,  which='major')
plt.gcf().axes[0].xaxis.grid(True,  which='major')
plt.gcf().axes[0].set_xticklabels([])
plt.gcf().axes[0].set_yticklabels([])
plt.gcf().axes[0].xaxis.set_ticks_position('none')
plt.gcf().axes[0].yaxis.set_ticks_position('none')
plt.tight_layout()# adjust figure to fit to labels

############################################################################
#save:

if os.path.isfile(FILE_NAME + ".svg") or os.path.isfile(FILE_NAME + ".csv"):
    if "n"==input("Do you want to replace the output-file(s)?[y/n]"):
        sys.exit()
plt.savefig(FILE_NAME + ".svg")

with open(FILE_NAME+".csv", "w") as file:
    writer = csv.writer(file)
    i=0
    while i<len(x_list):
        writer.writerow([x_list[i],y_list[i]])
        i += 1
        
plt.show()
