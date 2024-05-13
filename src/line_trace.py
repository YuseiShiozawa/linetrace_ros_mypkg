#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32

import cv2

def main():
    rospy.init_node('distance_publisher', anonymous=True)
    pub = rospy.Publisher('distance', Int32, queue_size=10)
    rate = rospy.Rate(10)  # ループ周波数（10Hz）

    cap = cv2.VideoCapture(4)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cv2.namedWindow('video image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('video image', 85, 60)

    blue_point_x1 = 100 # 左の青点
    blue_point_y1 = 60
    blue_point_x2 = 550 # 右の青点
    blue_point_y2 = 60 

    while not rospy.is_shutdown():
        ret, img = cap.read()

        height, width, _ = img.shape
        img = img[height//2:, :]
        red_point_x = width // 2
       # cv2.imshow('video image', img)
   
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])

                distance = (cx - red_point_x) * -1

                if blue_point_y1 >= 0 and blue_point_y1 < img.shape[0] and blue_point_x1 >= 0 and blue_point_x1 < img.shape[1]:
                    if binary[blue_point_y1, blue_point_x1] != 0:
#                        distance = 77777
                        if blue_point_y2 >= 0 and blue_point_y2 < img.shape[0] and blue_point_x2 >= 0 and blue_point_x2 < img.shape[1]:
                            if binary[blue_point_y2, blue_point_x2] != 0:
                                distance = 77777
 
                pub.publish(distance)
                rate.sleep()

        cv2.imshow('video image', img)
        cv2.waitKey(1)
    cap.release()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

