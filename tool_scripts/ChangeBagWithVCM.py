#!/usr/bin/env python

print "add  vcm to  bag ...."

import cv2
import csv
import os
import sys
import argparse
# import sm
import rosbag
import numpy as np
import urllib
import rospy
#import ImageFile

from added_msgs.msg import Image2

from sensor_msgs.msg import Image
from geometry_msgs.msg import Vector3Stamped
from std_msgs.msg import Time

try:
    import cv
    png_flag = cv.CV_IMWRITE_PNG_COMPRESSION
except ImportError:    
    png_flag = cv2.IMWRITE_PNG_COMPRESSION

from multiprocessing import Process, Manager, Queue, cpu_count, queues
from cv_bridge import CvBridge, CvBridgeError


#----------------------------------------------------parse params------------------------------------------------
parser = argparse.ArgumentParser(description = 'turn ARCore Data to ordinary bag')
parser.add_argument('--bag', metavar = 'bag', help = 'ARCore bag file')
parser.add_argument('--output-bag', metavar = 'output_bag', help = 'ROS bag file')
parsed = parser.parse_args()

#-----------------------------------------------------main()-------------------------------------------------------
camera_image_topics = {
	#'feature_tracking_primary/data'
	'/cam0/image_raw'
}
imu_topics = {
	#'sensor/data'
        '/acc0',
        '/gyr0',
        '/imu0'
}

bag_w = rosbag.Bag(parsed.output_bag, 'w')
bridge = CvBridge()

_G_TIMESTAMP_SHIFT = rospy.Duration(0) # set time offset 0

for topic, msg, timestamp in rosbag.Bag(parsed.bag).read_messages():
	if topic in camera_image_topics:
            timestamp += _G_TIMESTAMP_SHIFT
            rosimage = Image2()
            rosimage.vcm = 364
            rosimage.header.stamp = msg.header.stamp + _G_TIMESTAMP_SHIFT
            rosimage.height = msg.height
            rosimage.width = msg.width
            rosimage.step = rosimage.width
            rosimage.encoding = "mono8"
            rosimage.data = msg.data
            bag_w.write(topic, rosimage, timestamp)

	if topic in imu_topics:
            timestamp += _G_TIMESTAMP_SHIFT
            msg.header.stamp += _G_TIMESTAMP_SHIFT
            bag_w.write(topic, msg, timestamp)

bag_w.close()
        



























