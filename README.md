# readout_ultrasonic_1090
Readout data from ultrasonic Echograph 1090 (limited protocol)

# Description:
This is a quick-and-dirty solution to get the displayed graph from the ultrasonic device Karl Deutsch Echograph 1090 via USB to the computer. 
Under Linux, the device is attached as a virtual serial connection. This Python3-script transfers the RAW-data via this connection to the computer and stores the displayed graph as *.svg and *.csv.

# Tested configuration:
 - Linux Host System: Debian Stretch
 - Python3.5
 
# Quick start:
Just set the path to the device (serial port) and the filename for the graph in the config-section of the script and run the script without any parameter. 
Make sure that you have the rights to access the serial port.
