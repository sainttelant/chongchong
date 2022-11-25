import cv2
import sys


if __name__ == "__main__":
    radar_no = str(sys.argv[1])
    radar_camera = {'81': ['11.89.197.8', 'admin', 'qianfang123'],
                    '82': ['11.89.197.2', 'admin', 'qianfang123'],
                    '83': ['11.89.197.6', 'admin', 'qianfang123'],
                    '84': ['11.89.197.4', 'admin', 'qianfang123'],
                    '215': ['10.203.204.198', 'admin', 'Ucit2021']}
    if not radar_camera.get(radar_no):
        print('ERROR radar number: %s' % radar_no)
        exit(-1)

    address, user, pwd = radar_camera[radar_no]
    video_src = 'rtsp://%s:%s@%s:554/ch1/sub/av_stream' % (user, pwd, address)
    print(video_src)
    cap = cv2.VideoCapture(video_src)
    h, w = 500, 1000
    scale = 0.85
    while cap.isOpened():
        ret, frm = cap.read()
        frm = frm[:h, :w]
        # frm = cv2.resize(frm, (int(w*scale), int(h*scale)))

        frm = cv2.resize(frm, (500, 500))
        frm = frm[0:-100, 100:]
        #cv2.circle(frm, (89, 195), 25, (0, 0, 255), lineType=cv2.LINE_AA)
        # cv2.circle(frm, (120, 70), 25, (0, 0, 255), lineType=cv2.LINE_AA)

        cv2.namedWindow('camera-215', cv2.WINDOW_NORMAL)
        cv2.imshow('camera-215', frm)
        key = cv2.waitKey(1)
        if key == 27:
            exit(0)


