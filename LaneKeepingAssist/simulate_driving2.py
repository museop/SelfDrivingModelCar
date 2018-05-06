import cv2
import numpy as np
import argparse
import os
from steering_model import SteeringModel
from utility import load_image, radian2degree

steering_model = None

def simulate_driving(args):
    cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)320, height=(int)160,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
    wheel_img = cv2.imread('wheel.jpg', 0)
    rows, cols = wheel_img.shape

    while True:
        ret, image = cap.read()
        cv2.imshow('image', image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        steering_radian = steering_model.predict(image)
        steering_degree = radian2degree(steering_radian)

        M = cv2.getRotationMatrix2D((cols/2, rows/2), -2*steering_degree, 1)
        dst = cv2.warpAffine(wheel_img, M, (cols, rows))
        cv2.imshow("wheel", dst)

        key = cv2.waitKey(10)

        if key & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulate Driving')
    parser.add_argument('-m', help='path to model h5 file.', dest='model', type=str, default='model.h5')
    parser.add_argument('-d', help='data directory',         dest='data_dir', type=str, default='data')
    args = parser.parse_args()

    steering_model = SteeringModel()
    steering_model.load_model_from(args.model)
    simulate_driving(args)