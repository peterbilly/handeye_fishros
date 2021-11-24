#!/usr/bin/env python3
# coding: utf-8
"""
手眼标定测试程序，眼在手上
输入：
1.aruco码在相机坐标系下的坐标 camera_frame->aruco_marker_frame
2.手眼标定结果base_link->camera_frame
输出：
1.aruco码在机械臂基坐标下的位置,base_link->aruco_maker_frame

单独测试代码：
1.rosrun tf2_ros static_transform_publisher 0 0 0 0 0 0 1 base_link link7_name
2.rosrun tf2_ros static_transform_publisher 0 0 2 0 0 0 1 camera_frame aruco_marker_frame
3.roslaunch handeye-calib test_hand_on_eye_calib.launch

"""
import rospy
import tf
import transforms3d as tfs
from tf2_msgs.msg import TFMessage
import geometry_msgs.msg
import sys
import numpy as np
import math
import json
  

if __name__ == '__main__':
    rospy.init_node('test_hand_on_eye')   
    base_link = rospy.get_param("/test_hand_on_eye/base_link")
    end_link = rospy.get_param("/test_hand_on_eye/end_link")
    camera_link = rospy.get_param("/test_hand_on_eye/camera_link")
    marker_link = rospy.get_param("/test_hand_on_eye/marker_link")

    end_link2camera_link = rospy.get_param("/test_hand_on_eye/end_link2camera_link")
    end_link2camera_link = json.loads(end_link2camera_link.replace("'",'"'))

    listener = tf.TransformListener()
    br = tf.TransformBroadcaster()  

    rate = rospy.Rate(20.0)
    count = 0
    while not rospy.is_shutdown():
        try:
            (trans2,rot2) = end_link2camera_link['t'], end_link2camera_link['r']
            br.sendTransform(trans2,rot2,rospy.Time.now(),camera_link,end_link)
            
            if count>20:
                (trans1,rot1) = listener.lookupTransform(base_link,marker_link, rospy.Time(0))
                print("result:%s->%s, %s,%s" % (base_link,marker_link,trans1,rot1))
                count = 0
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        rate.sleep()