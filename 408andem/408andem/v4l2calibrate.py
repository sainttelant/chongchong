import sys
import cv2
import time
import datetime
import os

def read_cam(path):
    cap = cv2.VideoCapture("nvv4l2camerasrc ! video/x-raw(memory:NVMM), format=(string)UYVY, width=(int)2560, height=(int)1440 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
    if cap.isOpened():
        #cv2.namedWindow("demo", cv2.WINDOW_AUTOSIZE)
        while True:
            ret_val, img = cap.read();
            #img2 = cv2.cvtColor(img, cv2.COLOR_YUV2BGR_I420);
            #cv2.imshow('demo',img)
            timestamp = int(time.time()*1000)
            cv2.imwrite(path+str(timestamp)+".jpg",img)
            #cv2.waitKey(1)
            key = cv2.waitKey(1)
            if key == 27:
                exit(0)
    else:
        print("camera open failed")

    #cv2.destroyAllWindows()


if __name__ == '__main__':

    now = datetime.datetime.now()
    currentdate = now.strftime("%Y-%m-%d")
    print(currentdate)
    
    
    abspath = os.getcwd()
    if not os.path.exists(abspath+"imgs/%s/"%(currentdate)):
        os.makedirs(abspath+"imgs/%s/"%(currentdate))
        print("create folder for video recording!")
    recordpath = abspath+"imgs/%s/"%(currentdate)
    read_cam(recordpath)
