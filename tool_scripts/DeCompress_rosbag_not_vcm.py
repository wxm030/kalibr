#!/usr/bin/env python

print "DeCompress images and generate New bag...."

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
        '/gyr0'
}


def packImageToRosMsgWithVCM(time_stamp, img_np, vcm):
    """
    :param time_stamp:
    :param img_np:
    :return:
    """
    time_stamp += _G_TIMESTAMP_SHIFT

    rosimage = Image2()
    rosimage.vcm = vcm
    rosimage.header.stamp = time_stamp
    rosimage.height = img_np.shape[0]
    rosimage.width = img_np.shape[1]
    rosimage.step = rosimage.width
    rosimage.encoding = "mono8"
    rosimage.data = img_np.tostring()

    return rosimage, time_stamp


def packImageToRosMsg(time_stamp, img_np):
    """
    :param time_stamp:
    :param img_np:
    :return:
    """
    time_stamp += _G_TIMESTAMP_SHIFT

    rosimage = Image()
    rosimage.header.stamp = time_stamp
    rosimage.height = img_np.shape[0]
    rosimage.width = img_np.shape[1]
    rosimage.step = rosimage.width
    rosimage.encoding = "mono8"
    rosimage.data = img_np.tostring()

    return rosimage, time_stamp


bag_w = rosbag.Bag(parsed.output_bag, 'w')
bridge = CvBridge()

_G_TIMESTAMP_SHIFT = rospy.Duration(0) # set time offset 0

for topic, msg, timestamp in rosbag.Bag(parsed.bag).read_messages():
	if topic in camera_image_topics:
            nparr = np.fromstring(msg.data, np.uint8)
            img_decode = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
            image_msg, timestamp = packImageToRosMsg(timestamp, img_decode)
            #image_msg, timestamp = packImageToRosMsgWithVCM(timestamp, img_decode, msg.vcm)
            bag_w.write(topic, image_msg, timestamp)

	if topic in imu_topics:
            timestamp += _G_TIMESTAMP_SHIFT
            msg.header.stamp += _G_TIMESTAMP_SHIFT
            bag_w.write(topic, msg, timestamp)

bag_w.close()
        



























