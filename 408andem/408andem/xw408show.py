import sys
import math
import cv2
import numpy as np
import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
#from ecal.core.subscriber import StringSubscriber
import json
import RadarObject_pb2

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


def translate_x(_x):
    return abs(float((float(_x) - max_distance / 2) * scale_x) - float(edge / 2))


def translate_y(_y):
    return -float(_y) * scale_y + float(edge / 2)


y_pos = 7
x_pos = 39.9
w_, l_ = 3.4, 12

#右转碰线
rightturn_pos = y_pos

rightturn_x_start = 39.9
rightturn_x_end = 25



def has_turn_right(x, y):
    if rightturn_x_end+l_>x> rightturn_x_end and y > rightturn_pos> y -w_:
        return True
    else:
        return False


def has_enter_coil(x, y):
    return x_pos + l_ > x > x_pos and y_pos > y > y_pos - w_

def has_moving_straightway(x,y):
    return rightturn_x_end+l_ >x > rightturn_x_end and rightturn_pos> y > rightturn_pos-w_

def main(radar_no):
    print("eCAL {} ({})\n".format(ecal_core.getversion(), ecal_core.getdate()))
    ecal_core.initialize(sys.argv, "cluster_receive")
    ecal_core.set_process_state(1, 1, "I feel good")
    sub408 = ProtoSubscriber("ARS4G0_ObjectListPb%s" % radar_no,RadarObject_pb2.RadarObject)
    #sub408 = StringSubscriber("Txt%s" % radar_no)
    enter_coil_ids = set()
    enter_coil_count = 0

    analysis_turnright_ids = set()
    turn_right_count =  0 

    analysis_moving_straight_ids= set()
    move_straightway_count = 0


    azimuth = 0.0
    radar_azimuth = {'81': -0.03491, '82': 0.06702, '83': 0.0, '84': 0.0, '215': 0.0}
    radar_stop_line = {'81': [30, 50, 53.1], '82': [28, 50, 53.4], '83': [27, 47, 50.8], '84': [34, 56, 59.35], '215': [20, 25, 34.9]}
    radar_lane_line = {
        '81': [6.27, 3.27, 0.26, -2.72, -5.8, -9.14, -12.48, -15.79, -19.03, -22.33],
        '82': [5.56, 1.96, -1.54, -5.04, -6.4, -9.91, -13.43],
        '83': [9.54, 7.05, 3.7, 0.68, -2.3, -5.61, -9.67, -12.7, -15.66, -19.01],
        '84': [7.54, 3.87, 0.36, -3.15, -4.5, -8, -11.51],
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
    cv2.putText(img_tpl,"Coil",(int(translate_y(y_pos+3)),int(translate_x(x_pos-1))), cv2.FONT_ITALIC, 0.6, (0, 0, 0), 2)
    cv2.rectangle(img_tpl, (int(translate_y(y_pos)), int(translate_x(x_pos))), (int(translate_y(y_pos-w_)), int(translate_x(x_pos+l_))), (255, 0, 0))

   
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
    for ml in meas_line:
        _ml = ml
        ml = int(translate_x(ml))
        cv2.line(img_tpl, (0, ml), (edge, ml), (255, 255, 0))
        cv2.putText(img_tpl, '%3d' % _ml, (10, ml), cv2.FONT_ITALIC, 0.4, (0, 0, 0), 1)

    img = np.copy(img_tpl)
    remain_deleted = []
    old_em_msg = ''
    
     #统计右转车道的设计与算法
    cv2.line(img_tpl, (int(translate_y(rightturn_pos)),int(translate_x(rightturn_x_start))), \
        (int(translate_y(rightturn_pos)),int(translate_x(rightturn_x_end))),(100,100,100),2)
    
    i = 0
    while ecal_core.ok():
        _, msg, _ = sub408.receive(500)
        if msg == '':
            continue


        info = 'EnterTotal:%d' % enter_coil_count
        cv2.putText(img, info, (int(translate_y(25)), int(translate_x(80))), cv2.FONT_ITALIC, 0.6, (255, 0, 0), 1)

        #统计右转
        info = 'TurnRight:%d' % turn_right_count
        cv2.putText(img, info, (int(translate_y(25)), int(translate_x(70))), cv2.FONT_ITALIC, 0.6, (255, 0, 0), 1)
        #统计继续前行

        info = 'move_straight:%d' % move_straightway_count
        cv2.putText(img, info, (int(translate_y(25)), int(translate_x(60))), cv2.FONT_ITALIC, 0.6, (255, 0, 0), 1)
        
        i += 1
        if i >= 1:
            cv2.imshow('pc0%s' % radar_no, img)
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

        count = 0
        frame_ids = set()	
        flag = True
        for ele in msg.data:
            _id = ele.obj_id
            x = ele.obj_long_displ_m
            y = ele.obj_lat_displ_m
            vx = ele.obj_vrel_long_ms
            vy = ele.obj_lat_speed_ms
            prop = ele.obj_dyn_prob
            rcs= ele.obj_rcs_value_d_bm2
            measState = ele.obj_meas_stat
            poe =ele.obj_prob_of_exist
            _l = ele.obj_length
            _w =ele.obj_width
            class_type = ele.obj_class
            #print(_id,x,y,vx,vy,prop,rcs,measState,poe,_l,_w,class_type)
            if flag:
                if float(x) > max_distance:
                    continue
                
                count += 1
                frame_ids.add(_id)

                _rcs = rcs
                _x, _y = x, y
                vx, vy = float(vx), float(vy)
                _vx, _vy = vx, vy
                vx = math.cos(azimuth) * _vx - math.sin(azimuth) * _vy
                vy = math.cos(azimuth) * _vy + math.sin(azimuth) * _vx

                orientation = math.atan2(abs(-vy), abs(vx))
                if vx >= 0 and -vy <= 0:
                    orientation = -orientation
                elif vx <= 0 and -vy >= 0:
                    orientation = math.pi - orientation
                elif vx <= 0 and -vy <= 0:
                    orientation = -math.pi + orientation
                orientation = wrap_angle_once(orientation)

                xs, ys = float(x), float(y)
                x = math.cos(azimuth) * xs - math.sin(azimuth) * ys
                y = math.cos(azimuth) * ys + math.sin(azimuth) * xs

                if _id not in enter_coil_ids:
                    if has_enter_coil(x, y):
                        if abs(orientation) < math.pi/4 or abs(abs(orientation) - math.pi) < math.pi/4:
                            enter_coil_ids.add(_id)
                            enter_coil_count += 1  
                            if _id not in analysis_turnright_ids:
                                if has_turn_right(x, y):
                                    analysis_turnright_ids.add(_id)
                                    turn_right_count+=1
                        else:
                            print('OOO:%s,%d', _id, orientation)
                if _id not in analysis_moving_straight_ids:
                    if has_moving_straightway(x, y):
                        move_straightway_count+=1
                        analysis_moving_straight_ids.add(_id)            
                
                if _id not in analysis_turnright_ids:
                    if has_turn_right(x,y):
                        turn_right_count+=1
                        analysis_turnright_ids.add(_id)

                    
                # x = abs(float((float(x) - max_distance/2) * scale_x) - float(edge/2))
                x = translate_x(x)
                # y = -float(y) * scale_y + float(edge/2)
                y = translate_y(y)
                if y < 0 or y > edge:
                    continue

                x, y = int(x), int(y)
                prop = int(prop)
                rcs = int(rcs)

                rcs *= 4
                r = g = b = 0
                if rcs > 0:
                    r = rcs
                    r = 255 if r > 255 else r
                else:
                    b = abs(rcs)
                    b = 255 if b > 255 else b

                cv2.circle(img, (y, x), 3, (b, g, r), thickness=1)
                arrow(img, orientation, y, x, 18, (b, g, r))

                #info = ' %s,X:%.2f,Y:%.2f' % (_id, _x, _y)
                info = ' %s' % _id
                cv2.putText(img, info, (y, x-1), cv2.FONT_ITALIC, 0.4, (b, g, r), 1)

                _l = float(_l)*5
                _w = float(_w)*5
                cv2.line(img, (y, int(x-_l/2)), (y, int(x+_l/2)), (b, g, r))
                cv2.line(img, (int(y-_w/2), x), (int(y+_w/2), x), (b, g, r))
        
        
        

        for eci in enter_coil_ids.copy():
            if eci not in frame_ids:
                enter_coil_ids.remove(eci)
           
        for movstr in analysis_moving_straight_ids.copy():
            if movstr not in frame_ids:
                analysis_moving_straight_ids.remove(movstr)

        for turnids in analysis_turnright_ids.copy():
            if turnids not in frame_ids:
                analysis_turnright_ids.remove(turnids)

        cv2.putText(img, '%d' % count, (5, 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 1)
        cv2.putText(img, 'azimuth: %.4f' % azimuth, (5, 50), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1)

       

      

if __name__ == "__main__":
    print("begin to tuning non-motor display!!<<<")
    radar_no = str(sys.argv[1])
    #radar_no = "215"
    main(radar_no)


