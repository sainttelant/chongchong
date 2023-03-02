import sys
import math
import cv2
import numpy as np
import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber

import json
import time 

import datetime


scale = 800./600.
edge = int(600 * scale)
max_distance = 270
scale_y = 8.0 * scale
scale_x = math.floor(edge / max_distance)

def angle_diff(a, b):
    d1 = a - b
    d2 = 2 * math.pi - abs(d1)
    if d1 > 0:
        d2 *= -1.0
    if abs(d1) < abs(d2):
        return d1
    else:
        return d2


def wrap_angle_once(angle):
    wrap = angle
    if angle > math.pi:
        wrap -= (2 * math.pi)
    if angle < -math.pi:
        wrap += (2 * math.pi)
    return wrap


def arrow(img, orientation, x, y, len, cl=(0, 0, 0), thickness=1):
    angle = orientation + math.pi / 2.
    alpha = 30.

    _x = x + len * math.cos(angle + math.pi * alpha / 180.)
    _y = y + len * math.sin(angle + math.pi * alpha / 180.)
    _x, _y = int(_x), int(_y)
    cv2.line(img, (x, y), (_x, _y), cl, thickness=thickness)

    _x = x + len * math.cos(angle - math.pi * alpha / 180.)
    _y = y + len * math.sin(angle - math.pi * alpha / 180.)
    _x, _y = int(_x), int(_y)
    cv2.line(img, (x, y), (_x, _y), cl, thickness=thickness)

#转成图像坐标
def translate_x(_x):
    return abs(float((float(_x) - max_distance / 2) * scale_x) - float(edge / 2))


def translate_y(_y):
    return -float(_y) * scale_y + float(edge / 2)

#这个位置是修改线圈位置的，x代表纵向，y代表横向
y_pos = 10
x_pos = 66
w_, l_ = 3.4, 12


class MovingObj:

    def __init__(self, id,rId,info,timeupdate,timein,X_start, X_position,Y_position,length,width, curspeed, \
        orientation,lane,acceleration, altitude, RCS,CF,accessCount,accessflag):
        self.id = id
        self.rId = rId
        self.info = info
        self.timeupdate = timeupdate
        self.Y_position =Y_position
        self.curspeed = curspeed
        self.orientation = orientation
        self.lane = lane
        self.acceleration = acceleration
        self.altitude = altitude
        self.RCS = RCS
        self.CF = CF
        self.timein = timein
        self.X_position = X_position
        self.X_start = X_start
        self.length = length
        self.width = width
        self.speed = 0
        self.accessCount = 1
        self.accessflag = False
        self.sumspeed = 0
    
    def has_enter_anverage_speed_line(self):

        if (self.X_start>self.X_position) and (self.Y_position > -2):
            return True
        else:
            return False
        #return self.X_start > self.X_position
    
    def calculate_instant_speed(self):
        speed=3.6*(X_start-self.X_position)/(0.07*self.accessCount)
        self.speed = speed
        #print("average speed:",self.speed)

    def calc_speed(self):
        self.sumspeed += self.curspeed
        self.accessCount+=1
        self.speed = self.sumspeed/self.accessCount


def has_enter_coil(x, y):
    return x_pos + l_ > x > x_pos and y_pos > y > y_pos - w_


   

def main(radar_no,houzhui):
    print("eCAL {} ({})\n".format(ecal_core.getversion(), ecal_core.getdate()))
    ecal_core.initialize(sys.argv, "cluster_receive")
    ecal_core.set_process_state(1, 1, "I feel good")
    sub408 = StringSubscriber("Txt%s" % radar_no)
    if houzhui=="":
        sub_em = StringSubscriber("structTrack%s" % radar_no)
    else:
        sub_em = StringSubscriber("structTrack%s%s" % (houzhui,radar_no))

    enter_coil_ids = set()
    enter_coil_count:int = 0

    azimuth = 0.0
    #雷达相当于车道线的角度值,弧度值,上位机上面调,(上位机是角度,要转成弧度)
    radar_azimuth = {'81': -0.03491, '82': 0.06702, '83': 0.0, '84': 0.0, '215': 0.0}
    radar_stop_line = {'81': [30, 50, 53.1], '82': [28, 50, 53.4], '83': [27, 47, 50.8], '84': [34, 56, 59.35], '215': [20, 25, 34.9]} #第一个是盲区,39.9表示停止线,30表示停止线前移,为了统计效果
    radar_lane_line = {
        '81': [6.27, 3.27, 0.26, -2.72, -5.8, -9.14, -12.48, -15.79, -19.03, -22.33],
        '82': [5.56, 1.96, -1.54, -5.04, -6.4, -9.91, -13.43],
        '83': [9.54, 7.05, 3.7, 0.68, -2.3, -5.61, -9.67, -12.7, -15.66, -19.01],
        '84': [7.54, 3.87, 0.36, -3.15, -4.5, -8, -11.51],
        #从上位机调好,然后录进去
        '215': [9.8,7.1,3.5,0.5,-3,-6.4,-9.8,-13,-15.4]}
    if radar_azimuth.get(radar_no):
        azimuth = radar_azimuth[radar_no]

    #画各种车线
    stop_line = radar_stop_line.get(radar_no)
    lane_line = radar_lane_line.get(radar_no)
    #meas_line = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 200, 250]
    meas_line = [ 20,  60, 80,  100,  120, 140, 160, 200, 240]
    # img_template
    img_tpl = np.ones((edge, edge, 3), np.uint8)
    img_tpl *= 255
    #画雷达安装位置
    #Y 坐标左正右负
    cv2.putText(img_tpl,"Radar",(int(translate_y(-2)),int(translate_x(-1))), cv2.FONT_ITALIC, 0.6, (0, 0, 0), 2)
    cv2.circle(img_tpl, (int(translate_y(0)), int(translate_x(0))), 3, (255, 0, 0), thickness=5)

    #画真实的线圈,
    #cv2.circle(img_tpl, (int(translate_y(8.5)), int(translate_x(72))), 25, (0, 0, 255))

    # 线圈是矩形,用户真实需要的需求
    """
    cv2.putText(img_tpl,"Coil",(int(translate_y(y_pos+3)),int(translate_x(x_pos-1))), cv2.FONT_ITALIC, 0.6, (0, 0, 0), 2)
    cv2.rectangle(img_tpl, (int(translate_y(y_pos)), int(translate_x(x_pos))), (int(translate_y(y_pos-w_)), int(translate_x(x_pos+l_))), (255, 0, 0))
    """
    # 画停止线
    counter=0
    for sl in stop_line if stop_line is not None else []:
        sl = int(translate_x(sl))
        if counter ==0:
            pass
        else: 
            cv2.putText(img_tpl,"Radar StopD",(10, sl), cv2.FONT_ITALIC, 0.6, (0, 0, 0), 2)
        cv2.line(img_tpl, (0, sl), (edge, sl), (0, 0, 255))
        counter+=1
    #画车道线
    for ll in lane_line if lane_line is not None else []:
        ll = int(translate_y(ll))
        cv2.line(img_tpl, (ll, 0), (ll, edge), (0, 0, 255))
    #画测量线,横线判定距离的
    for ml in meas_line:
        _ml = ml
        ml = int(translate_x(ml))
        cv2.line(img_tpl, (0, ml), (edge, ml), (255, 255, 0))
        cv2.putText(img_tpl, '%3d' % _ml, (10, ml), cv2.FONT_ITALIC, 0.4, (0, 0, 0), 1)
    #img_tpl是模板，划线的模板
    img = np.copy(img_tpl)
    imgdels = np.copy(img_tpl)
    remain_deleted = []
    old_em_msg = ''


    # 维护的OBj 队列
    dict_MovingObjs={}



    i = 0
    cv2.namedWindow("pc0%s"%radar_no,1)
    while ecal_core.ok():
        _, msg, _ = sub408.receive()
        if msg == '':
            pass

        #打印出数字出来
        """
        info = '%d' % enter_coil_count
        cv2.putText(img, info, (int(translate_y(15)), int(translate_x(65))), cv2.FONT_ITALIC, 0.9, (255, 0, 0), 1)
        """
        i += 1
        if i >= 1:
            cv2.imshow('pc0%s' % radar_no, img)
            cv2.imshow("em_dels%s"%(radar_no),imgdels)
            key = cv2.waitKeyEx(1)
            if key == 27:  # Esc
                ecal_core.finalize()
                cv2.destroyAllWindows()
                exit(0)
            elif key == 43:  # +
                azimuth += 0.01
            elif key == 45:  # -
                azimuth -= 0.01
            elif key == 2490368:  # move up
                azimuth += 0.001
            elif key == 2621440:  # move down
                azimuth -= 0.001
            elif key == 2555904:  # ->(move right)
                img_tpl = np.ones((edge, edge, 3), np.uint8)
                img_tpl *= 255
                for i in range(len(lane_line)):
                    lane_line[i] -= 0.2
                    ll = int(translate_y(lane_line[i]))
                    cv2.line(img_tpl, (ll, 0), (ll, edge), (0, 0, 255))
                    #配车道线使用的，临时的tmp
                    print('%.2f' % lane_line[i], end=',')
                print('')
                pass
            elif key == 2424832:  # <-(move left)
                img_tpl = np.ones((edge, edge, 3), np.uint8)
                img_tpl *= 255
                for i in range(len(lane_line)):
                    lane_line[i] += 0.2
                    ll = int(translate_y(lane_line[i]))
                    cv2.line(img_tpl, (ll, 0), (ll, edge), (0, 0, 255))
                    print('%.2f' % lane_line[i], end=',')
                print('')
            if key != -1:
                print('key:%d' % key)

            i = 0
            img = np.copy(img_tpl)
            imgdels = np.copy(img_tpl)

        count = 0
        frame_ids = set()
     
        #针对em的画图
        _, msg, _ = sub_em.receive()
        if msg == '':
            msg = old_em_msg
            if msg == '':
                continue
        old_em_msg = msg
        j = json.loads(msg)

        currenttime = j.get("time")
        
        
        if j.get('objects') is None:
            continue
       
        # 当前帧的em输出对象集合
        a = [[obj, True] for obj in j['objects']]
        # 被删除对象的集合，瞬时删除的，特别维护了一段时间
        b = []
        if j.get('deleted') is not None:
            b = [[obj, True] for obj in j['deleted']]
        # 维护的帧到头了，删除的集合
        c = [[obj, False] for obj, n in remain_deleted if n > 0]

        

        for obj, from_em in a + b + c:
            #雷达的一个跟踪id，一个检测id
            _id = obj['id']
            _rId = obj.get('rId', -1)
            # 雷达测的即时速度
            _speed = obj["speed"]
            _x = obj['PosX']
            _y = obj['PosY']
            _info = obj['info']
            if _info == None:
                _info = "normal"
            _timeupdate = obj["time_since_last_update"]
            _l = obj["length"]
            _w = obj["width"]
            _lane = obj["lane"]
            _acceleration = obj["acceleration"]
            _altitude = 0 
            _RCS = obj["RCS"]
            _CF = obj["CF"]
            _orientation = obj["orientation"]
            
            movingObj = MovingObj(_id,_rId,_info,_timeupdate,0,200,_x,_y,_l,_w,_speed,_orientation, \
                _lane,_acceleration,_altitude,_RCS,_CF,1,False)
            
           


            # 进入平均车速计算环节
            if movingObj.has_enter_anverage_speed_line() or movingObj.accessflag== True: 
                movingObj.accessflag = True
                in_movingObj = { _id: movingObj }

                if movingObj.id not in dict_MovingObjs.keys():
                   
                    dict_MovingObjs.update(in_movingObj)
                   
                else:
                    dict_MovingObjs[_id].curspeed = _speed
                    dict_MovingObjs[_id].X_position = _x
                    dict_MovingObjs[_id].Y_position = _y
                    dict_MovingObjs[_id].accessCount+=1
         
            

            #em输出弧度，转成角度
            _orientation = _orientation / 180.0 * math.pi

            #最好一次更新的时间

            _time_since_last_update = obj.get('time_since_last_update')
            
            if _time_since_last_update is None:
                _time_since_last_update = 0.0

            #翻译成pixel 像素
            x = abs(float((float(_x) - max_distance / 2) * scale_x) - float(edge / 2))
            y = -float(_y) * scale_y + float(edge / 2)
            if y < 0 or y > edge:
                continue
            x, y = int(x), int(y)
            thickness = 1

            if -1 != _info.find('deleted;')\
                    or -1 != _info.find('be_merged;'):
                
                #被合并或者删除，画灰色
                cl = (180, 0, 160)
                movingObj.info= "deleted_be_merged"
                thickness = 1
                if from_em:
                    remain_deleted.append([obj, 13])
            #表示没有检测目标的
            elif _rId == -1:
                #蓝色代表预测的
                cl = (255, 0, 0)
                movingObj.info = "pre"
            else:
                #新生成的对象是紫色的
                if -1 != _info.find('new;'):
                    cl = (255, 0, 255)
                    movingObj.info = "new_Det"
                    # thickness = 3
                #禁止合并，
                elif -1 != _info.find('disable_merge;'):
                    #红色
                    cl = (0, 0, 255)
                    movingObj.info="disable_merge"
                elif -1!=_info.find('force_merge'):
                    cl =(0,100,255)
                    movingObj.info = "force_merge"  
                else:
                    #检测到的目标 绿色
                    cl = (0, 150, 0)

            if -1 != _info.find('new_merged;'):
                thickness = 1
                movingObj.info ="new_M"
            # 瞬时的时刻，虽然合并了，但是角度偏差大，需要特别注意下，有可能错误关联上的目标
            if -1 != _info.find('!radian;'):
                b_radian = True
                # print("!radian:", _id)
                cv2.putText(img, 'R', (y, x), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 1)
            
            if -1 != _info.find('Rollback!'):
              
                # print("!radian:", _id)
                cv2.putText(img, 'Rollback', (y, x), cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 0, 255), 1)    

            
            if -1 == _info.find('deleted;'):
                #cv2.circle(img, (y, x), 13, cl, thickness)
                cv2.putText(img,movingObj.info,(y-3,x+5),cv2.FONT_ITALIC,0.4,cl,thickness)
            else:
                cv2.line(img, (y - 6, x - 6), (y + 6, x + 6), cl, thickness)
                cv2.line(img, (y + 6, x - 6), (y - 6, x + 6), cl, thickness)
                if -1 != _info.find('in_blind_area;'):
                    #出了监控画矩形
                    cv2.rectangle(img, (y - 7, x - 7), (y + 7, x + 7), cl, 2)
            arrow(img, _orientation, y, x, 12, cl, 1)

            # info = '%d,%.2f' % (_id, _orientation)
            #info = '%d-%.1f' % (_id, _time_since_last_update)

            
            for allobj_dict in dict_MovingObjs.values():
                allobj_dict.calc_speed()
            
            average_speed =0 
            try:
                average_speed = dict_MovingObjs[_id].speed
            except:
                average_speed = 0

            #info = '%d_%.2f_AVSP_%.3f' % (_id,_speed,average_speed)
            info = '%d:_orite_%.2f' %(_id,_orientation)
            cv2.putText(img, info, (y, x + 15), cv2.FONT_ITALIC, 0.36, (255, 0, 0), 1)
            

        #根据最多保持多少帧的要消逝的目标
        remain_deleted = [[obj, n - 1] for obj, n in remain_deleted if n >1]
        for delsobj,nums in remain_deleted:
            #print("delsobj:",delsobj)
            _delsinfo = delsobj["info"]
            _delsinfo.replace("deleted;","")
           
            _delsid = str(delsobj["id"])
            if -1!= _delsinfo.find("stoppedbuttraveledtooless"):
                print("delsobj's rId:",delsobj["id"],delsobj["info"])
                cv2.putText(imgdels, _delsid+"_"+_delsinfo[7:],(y-3,x+5),cv2.FONT_ITALIC,0.6,cl,thickness)
                cv2.line(imgdels, (y - 9, x - 9), (y + 9, x + 9), cl, thickness)
                cv2.line(imgdels, (y + 9, x - 9), (y - 9, x + 9), cl, thickness)
                cv2.waitKey(300)
            if -1!= _delsinfo.find("stoppedtimegreat0.3"):
                #print("delsobj's rId:",delsobj["id"],delsobj["info"])
                #print("delsobj's rId:",delsobj["id"],delsobj["info"])
                cv2.putText(imgdels,_delsid+"_"+_delsinfo[7:],(y-3,x+5),cv2.FONT_ITALIC,0.6,cl,thickness)
                cv2.line(imgdels, (y - 9, x - 9), (y + 9, x + 9), cl, thickness)
                cv2.line(imgdels, (y + 9, x - 9), (y - 9, x + 9), cl, thickness)
                cv2.waitKey(300)
            if -1!= _delsinfo.find("dynamicgreatexpi"):
                #print("delsobj's rId:",delsobj["id"],delsobj["info"])
                #print("delsobj's rId:",delsobj["id"],delsobj["info"])
                cv2.putText(imgdels,_delsid+"_"+_delsinfo[7:],(y-3,x+5),cv2.FONT_ITALIC,0.6,cl,thickness)
                cv2.line(imgdels, (y - 9, x - 9), (y + 9, x + 9), cl, thickness)
                cv2.line(imgdels, (y + 9, x - 9), (y - 9, x + 9), cl, thickness)
                cv2.waitKey(300)
            if -1!= _delsinfo.find("dynamicupdategreat0.2"):
                #print("delsobj's rId:",delsobj["id"],delsobj["info"])  
                #print("delsobj's rId:",delsobj["id"],delsobj["info"])
                cv2.putText(imgdels,_delsid+"_"+_delsinfo[7:],(y-3,x+5),cv2.FONT_ITALIC,0.6,cl,thickness)
                cv2.line(imgdels, (y - 9, x - 9), (y + 9, x + 9), cl, thickness)
                cv2.line(imgdels, (y + 9, x - 9), (y - 9, x + 9), cl, thickness)
                cv2.waitKey(300)
            if -1!= _delsinfo.find("EoF"):
                #print("delsobj's rId:",delsobj["id"],delsobj["info"])  
                #print("delsobj's rId:",delsobj["id"],delsobj["info"])
                cv2.putText(imgdels,_delsid+"_"+_delsinfo[7:],(y-3,x+5),cv2.FONT_ITALIC,0.6,cl,thickness)
                cv2.line(imgdels, (y - 9, x - 9), (y + 9, x + 9), cl, thickness)
                cv2.line(imgdels, (y + 9, x - 9), (y - 9, x + 9), cl, thickness)
                cv2.waitKey(300)
           

if __name__ == "__main__":
    print("begin to tuning non-motor display!!<<<")
    radar_no = str(sys.argv[1])
    try:

        suffix = str(sys.argv[2])
    except:
        print("default em show!")
        suffix = ""
    main(radar_no,suffix)
    
    


