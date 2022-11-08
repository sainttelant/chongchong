import cv2
import sys
import os
import skvideo.io

def recordmp4(c):
    while c.isOpened():
         ret, frm = cap.read()
         cv2.namedWindow('camera-215', cv2.WINDOW_NORMAL)
         cv2.imshow('camera-215', frm)
         out.writeFrame(frm)
         key = cv2.waitKey(1)
         if key == 27:
             exit(0)

"""""
def recordecal(a):
    print(a)
    subprocess.call(["ecal_rec.exe","-r","-n","ecal_mea","--whitelist","ARS4G0_ObjectListPb215","-d","F:/"],shell=True)
"""""


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


    if not os.path.exists("F:/ecal_mea/"):
        os.mkdir("F:/ecal_mea/")
    
    outputfile = "F:/ecal_mea/video.mp4"
    frame_fps = int(cap.get(cv2.CAP_PROP_FPS))
    # 获取视频帧宽度和高度
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print("video fps={},width={},height={}".format(frame_fps, frame_width, frame_height))
    out = skvideo.io.FFmpegWriter(outputfile,inputdict={'-r': str(frame_fps), '-s':'{}x{}'.format(frame_width,frame_height)}, outputdict={'-r': str(frame_fps), '-vcodec': 'libx264'})

    
    #p = Process(target=recordmp4(cap))
    #p.start()
    #p1 = Process(target = recordecal)
    #p1.start()

    #p.join()
    #p1.join()
   
    recordmp4(cap)



    out.close()
    cap.release()
    cv2.destroyAllWindows()
  


