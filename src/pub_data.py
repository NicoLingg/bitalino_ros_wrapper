#!/usr/bin/env python
from bitalino import BITalino
import rospy
from std_msgs.msg import Float32
from numpy import double
import numpy as np

global device


def clean_shutdown():
    global device
    # Stop acquisition
    device.stop()
    # Close connection
    device.close()


if __name__=="__main__":
    global device

    # ROS setups 
    rospy.init_node("bitalino")
    eda_data_pub = rospy.Publisher("/bitalino/eda", Float32, queue_size=10)
    temp_data_pub = rospy.Publisher("/bitalino/temp", Float32, queue_size=10)
    rospy.on_shutdown(clean_shutdown)


    # Bitalino setup
    #TODO - Move settings files to a config file
    macAddress = "20:16:12:22:45:58" 
    batteryThreshold = 30
    acqChannels = [0,4] 
    samplingRate = 1000 
    nSamples = 1

    # Connect to Bitalino and setup
    device = BITalino(macAddress)
    device.battery(batteryThreshold)
    rospy.loginfo(device.version())

    # Start data acquisition
    device.start(samplingRate, acqChannels)
    


    while not rospy.is_shutdown():
            # Read samples
            data_raw = device.read(nSamples)
            # data = data[:]
            #data = np.transpose(data)
            #data = data[-2:]
            #data_raw = np.transpose(data_raw)
            #data_raw = data_raw[-2:]
            
            # Conversion from here: https://bitalino.com/documentation
            temp_raw = double(data_raw[0][5])
            eda_raw = double(data_raw[0][6])
            temp_c = ((temp_raw/1024)*3.3-0.5)*100
            eda_uS = ((eda_raw/1024)*3.3)/0.12

            eda_data_pub.publish(eda_uS)
            temp_data_pub.publish(temp_c)


