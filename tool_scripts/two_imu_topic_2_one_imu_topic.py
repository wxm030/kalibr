#!/usr/bin/env python

print "two imu topic to one imu topic..."
import sys
import argparse
import rosbag
from sensor_msgs.msg import Image
from sensor_msgs.msg import Imu


#decleration
camera_image_topics = {'/cam0/image_raw'}
acc_topics = {'/acc0'}
gyr_topics = {'/gyr0'}

def createImuMessge(timestamp, omega0,omega1,omega2, alpha0,alpha1,alpha2):
    rosimu = Imu()
    rosimu.header.stamp = timestamp
    rosimu.angular_velocity.x = float(omega0)
    rosimu.angular_velocity.y = float(omega1)
    rosimu.angular_velocity.z = float(omega2)
    rosimu.linear_acceleration.x = float(alpha0)
    rosimu.linear_acceleration.y = float(alpha1)
    rosimu.linear_acceleration.z = float(alpha2)
    return rosimu, timestamp


def parseArgs():
    # setup the argument list
    parser = argparse.ArgumentParser(description='turn orbbec.bag Data to one imu  bag')
    parser.add_argument('--bag', metavar='bag', help='orbbec bag file')
    parser.add_argument('--output-bag', metavar='output_bag', default="output.bag", help='out ROS bag file')

    # print help if no argument is specified
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)

    # parse the args
    parsed = parser.parse_args()
    return parsed


def change_imu_topics(input_bag, output_bag):
    """
    change  acc and gyro topic to one imu topic
    :param input_bag:   input rosbag
    :param output_bag:  output rosbag
    :return:
    """

    bag_w = rosbag.Bag(output_bag, 'w')
    t_acc = []
    t_gyro = []
    ax_l = []
    ay_l = []
    az_l = []
    gx_l = []
    gy_l = []
    gz_l = []

    #read data from input bag
    for topic, msg, t in rosbag.Bag(input_bag).read_messages():
        #img data not change
        if topic in camera_image_topics:
            bag_w.write("/cam0/image_raw", msg, t)

        #extract imu data to array
        if topic in acc_topics:
            t_acc.append(t)
            ax_l.append(msg.vector.x)
            ay_l.append(msg.vector.y)
            az_l.append(msg.vector.z)
	if topic in gyr_topics:
            t_gyro.append(t)
            gx_l.append(msg.vector.x)
            gy_l.append(msg.vector.y)
            gz_l.append(msg.vector.z)

    #write imu data to outbag
    topic_f = 'imu0'
    if len(t_acc) > len(t_gyro):
        for i in range(len(t_gyro)):
            imumsg, timestamp = createImuMessge(t_gyro[i], gx_l[i],gy_l[i],gz_l[i], ax_l[i],ay_l[i],az_l[i])
            bag_w.write("/{0}".format(topic_f), imumsg, timestamp)
    else:
        for i in range(len(t_acc)):
            imumsg, timestamp = createImuMessge(t_acc[i], gx_l[i],gy_l[i],gz_l[i], ax_l[i],ay_l[i],az_l[i])
            bag_w.write("/{0}".format(topic_f), imumsg, timestamp)
    bag_w.close()

    return True

        
if "__main__" == __name__:
    parsed = parseArgs()
    if not parsed:
        sys.exit(101)

    ret = change_imu_topics(parsed.bag, parsed.output_bag)
    if not ret:
        sys.stderr.write("False" + "\n")
        sys.exit(101)

    sys.exit(0)

