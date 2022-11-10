# 时间占有率统计
import sys
import math
import threading

import cv2
import numpy as np
import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber
import json

scale = 720./600.
edge = int(600 * scale)
max_distance = 170
scale_y = 8.0 * scale
scale_x = math.floor(edge / max_distance)


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


class CMyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name='')
        self.lock = threading.Lock()
        self.frm = None

    def take(self):
        frm = None
        self.lock.acquire()
        if self.frm is not None:
            frm, self.frm = self.frm, frm
        self.lock.release()

        return frm

    def run(self):
        radar_no = '215'
        print('version: normal')
        last_time = 0
        last_cycle_stat_time = 0
        first_cycle_stat_time = 0
        last_frame_time = 0
        delay_stat = dict()  # _id: int, delay_seconds: float
        stop_stat = dict()   # _id: int, [stop_count: int, >5km/h: bool(default value is true)]
        obj_last_x = dict()  # _id: int, [last_x: float, time, lane_id]
        lane_stat = dict()   # lane_id, [pass_obj_count, sum_delay, sum_stop]
        lost_objs = dict()   # _id, [rear_ids: set, last_x, last_time, last_lane_id, delay, stop]
        queue_stat = dict()  # lane_id, max_length
        coil_stat = dict()  # coil_id, x, y, pass_count, sum_pulse_time
        velocity_stat = dict()  # _id, [sum_velocity, n]

        print("eCAL {} ({})\n".format(ecal_core.getversion(), ecal_core.getdate()))
        ecal_core.initialize(sys.argv, "cluster_receive")
        ecal_core.set_process_state(1, 1, "I feel good")
        sub_em = StringSubscriber("structTrack0%s" % radar_no)

        azimuth = 0.0
        radar_azimuth = {'81': -0.03491, '82': 0.06702, '83': 0.0, '84': 0.0}
        radar_stop_line = {'81': [30, 50, 53.1], '82': [28, 50, 53.4], '83': [27, 47, 50.8], '84': [34, 56, 59.35], '85': [125, 135, 135], '215': [20, 30, 39.9]}
        radar_lane_line = {
            '81': [6.27, (3.27, 10), (0.26, 9), (-2.72, 8), (-5.8, 7), -9.14, -12.48, -15.79, -19.03, -22.33],
            '82': [5.56, (1.96, 12), (-1.54, 11), -5.04, -6.4, -9.91, -13.43],
            '83': [9.54, (7.05, 4), (3.7, 3), (0.68, 2), (-2.3, 1), -5.61, -9.67, -12.7, -15.66, -19.01],
            '84': [7.54, (3.87, 6), (0.36, 5), -3.15, -4.5, -8, -11.51],
            '85': [(11.5, 1), (7, 2), (3.5, 3), (0, 4), -3.5, -13.5, -25.5],
            '215': [9.8, 7.1, 3.5, 0.5, -3, -6.4, -9.8, -13, -15.4]
        }
        radar_rectangle = {  # (x, y, l, w)
            '81': [(52.1, 6.27, 5., 18.75), (52.1, 3.27, 10., 3., (76, 129, 139)), (52.1, 6.27, 30., 3., (76, 129, 139))],
            '82': [(52.4, 5.56, 5., 11.96), (52.4, 1.96, 10., 3.5, (76, 129, 139)), (50., 5.56, 30., 3.6, (76, 129, 139))],
            '83': [(49.8, 9.54, 5., 19.21), (49.8, 7.05, 10., 3.35, (76, 129, 139)), (47., 9.54, 30., 2.49, (76, 129, 139))],
            '84': [(58.35, 7.54, 5., 12.04), (58.35, 3.87, 10, 3.51, (76, 129, 139)), (56, 7.54, 30, 3.67, (76, 129, 139))],
        }
        '''
        radar_coils = {  # (x, y, l, w, lane_id, coil_id)
            '85': [(50.0, 7.0, 3.0, 3.5, 2, 1), (50.0, 3.5, 3.0, 3.5, 3, 2), (50.0, 0.0, 3.0, 3.5, 4, 3),
                   (70.0, 7.0, 3.0, 3.5, 2, 4), (70.0, 3.5, 3.0, 3.5, 3, 5), (70.0, 0.0, 3.0, 3.5, 4, 6),
                   (100.0, 7.0, 3.0, 3.5, 2, 7), (100.0, 3.5, 3.0, 3.5, 3, 8), (100.0, 0.0, 3.0, 3.5, 4, 9), ]}
        '''
        radar_coils = {  # (x, y, l, w, lane_id, coil_id)
            '85': [(33.0, 3.5, 8.0, 3.5, 3, 1), ],
            '215': [(55.0, 9.8, 3.5, 2.7, 1, 1), (55.0, 7.1, 3.5, 3.6, 2, 2), (55.0, 3.5, 3.5, 3.5, 3, 3), (55.0, 0.5, 3.5, 3.5, 4, 4) ]}
        if radar_azimuth.get(radar_no):
            azimuth = radar_azimuth[radar_no]
        stop_line = radar_stop_line.get(radar_no)
        lane_line = radar_lane_line.get(radar_no)
        rect = radar_rectangle.get(radar_no)
        coil = radar_coils.get(radar_no)
        meas_line = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160]

        stop_line_for_stat = stop_line[2] - 1.0
        stop_line_for_queue = stop_line[2]
        start_line_for_velocity, end_line_for_velocity = stop_line[0], stop_line[2]
        # img_template
        img_tpl = np.ones((edge, edge, 3), np.uint8)
        img_tpl *= 255
        cv2.circle(img_tpl, (int(translate_y(0)), int(translate_x(0))), 3, (255, 0, 0), thickness=5)

        for sl in stop_line if stop_line is not None else []:
            sl = int(translate_x(sl))
            cv2.line(img_tpl, (0, sl), (edge, sl), (255, 0, 255))
        lane_line_y = []
        for ll in lane_line if lane_line is not None else []:
            lane_no = 0
            if type(ll) is tuple:
                lane_no = ll[1]
                ll = ll[0]
            ll = int(translate_y(ll))
            cv2.line(img_tpl, (ll, 0), (ll, edge), (0, 0, 255))
            if lane_no > 0:
                cv2.putText(img_tpl, '%2d' % lane_no, (ll, 720), cv2.FONT_ITALIC, 0.6, (0, 0, 0), 2)
                lane_line_y.append((lane_no, ll))
        for ml in meas_line:
            _ml = ml
            ml = int(translate_x(ml))
            cv2.line(img_tpl, (0, ml), (edge, ml), (255, 255, 0))
            cv2.putText(img_tpl, '%3d' % _ml, (10, ml), cv2.FONT_ITALIC, 0.4, (0, 0, 0), 1)
        for rc in rect if rect is not None else []:
            b = g = r = 0
            if len(rc) >= 5:
                b, g, r = rc[4]
            cv2.rectangle(img_tpl, (int(translate_y(rc[1])), int(translate_x(rc[0]+rc[2]))), (int(translate_y(rc[1]-rc[3])), int(translate_x(rc[0]))),
                          (b, g, r), thickness=1, lineType=cv2.LINE_AA)
        for cl in coil if coil is not None else []:
            cv2.rectangle(img_tpl, (int(translate_y(cl[1])), int(translate_x(cl[0]+cl[2]))), (int(translate_y(cl[1]-cl[3])), int(translate_x(cl[0]))),
                          (255, 0, 0), thickness=1, lineType=cv2.LINE_AA)
            cv2.putText(img_tpl, '%3d' % cl[5], (int(translate_y(cl[1])), int(translate_x(cl[0]))), cv2.FONT_ITALIC, 0.4, (255, 0, 0), 1)

        img = np.copy(img_tpl)
        remain_deleted = []
        old_em_msg = ''

        i = 0
        while ecal_core.ok():
            i += 1
            if i >= 1:
                for coil_x, coil_y, coil_pass_count, sum_pulse_time in coil_stat.values():
                    cv2.putText(img, '%dms' % int(sum_pulse_time * 1e+3), (int(translate_y(coil_y)), int(translate_x(coil_x)) + 15), cv2.FONT_ITALIC, 0.4, (0, 0, 0), 1)

                self.lock.acquire()
                self.frm = None
                img, self.frm = self.frm, img
                self.lock.release()

                i = 0
                img = np.copy(img_tpl)
                for ln, y in lane_line_y:
                    if queue_stat.get(ln) is not None:
                        max_length = int(translate_x(queue_stat[ln] + stop_line_for_queue))
                        cv2.line(img, (y, max_length), (y + 40, max_length), (0, 0, 255), thickness=2)

            _, msg, _ = sub_em.receive()
            if msg == '':
                msg = old_em_msg
                if msg == '':
                    continue
            old_em_msg = msg
            j = json.loads(msg)
            now = j['time']
            if last_time == 0:
                last_time = now
            if last_cycle_stat_time == 0:
                last_cycle_stat_time = now
                first_cycle_stat_time = now
                last_frame_time = now
            if j.get('objects') is None:
                continue

            cv2.putText(img, '%ds' % ((now - first_cycle_stat_time) / 1e+6), (660, 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 1)

            _obj_lanes = dict()
            a = [[obj, True, True] for obj in j['objects']]
            b = []
            if j.get('deleted') is not None:
                b = [[obj, True, False] for obj in j['deleted']]
            c = [[obj, False, False] for obj, n in remain_deleted if n > 0]
            ids = set()
            for obj, from_em, published in a + b + c:
                _id = obj['id']
                ids.add(_id)
                _lane_id = obj['lane']
                _obj_lanes[_id] = _lane_id
                _rId = obj.get('rId', -1)
                _x = obj['PosX']
                _y = obj['PosY']
                _info: str = obj.get('info', '')
                _orientation = obj['orientation']
                _orientation = _orientation / 180.0 * math.pi
                _speed = obj['speed']
                _time_since_last_update = obj.get('time_since_last_update')
                if _time_since_last_update is None:
                    _time_since_last_update = 0.0

                if published:
                    for lost_obj_id, lost_obj_info in lost_objs.items():
                        lo_rear_ids, lo_last_x, lo_last_time, lo_last_lane_id, lo_delay, lo_stop = lost_obj_info
                        if _id not in lo_rear_ids and _x >= lo_last_x and _lane_id == lo_last_lane_id:
                            lo_rear_ids.add(_id)

                    if stop_stat.get(_id) is None:
                        stop_stat[_id] = [0, True]
                    if stop_stat[_id][1]:
                        if _speed <= 1e-08:
                            stop_stat[_id][0] += 1
                            stop_stat[_id][1] = False
                    else:  # >5km/h is False
                        if _speed > 5:
                            stop_stat[_id][1] = True
                    if _speed < 5.0:
                        if delay_stat.get(_id) is None:
                            delay_stat[_id] = 0
                        delay_stat[_id] += float(now - last_time) / 1e+6
                    if _speed < 0.2:
                        if queue_stat.get(_lane_id) is None or queue_stat[_lane_id] < (_x + 5.0 - stop_line_for_queue):
                            queue_stat[_lane_id] = _x + 5.0 - stop_line_for_queue

                    if obj_last_x.get(_id) is not None:
                        for coil_x, coil_y, l, _, coil_lane_id, coil_id in coil:
                            if coil_stat.get(coil_id) is None:
                                coil_stat[coil_id] = [coil_x, coil_y, 0, 0.]
                            if _lane_id == coil_lane_id and (_x < coil_x < obj_last_x[_id][0]):
                                coil_stat[coil_id][2] += 1
                                coil_stat[coil_id][3] += (8. / (_speed / 3.6))
                                print('BBB', _speed, coil_stat[coil_id])
                            '''
                            if _lane_id == coil_lane_id and (coil_x < _x < coil_x + l):
                                print('AAA:', now, last_frame_time, now - last_cycle_stat_time)
                                coil_stat[coil_id][3] += (now - last_frame_time)
                            '''

                        if _x < stop_line_for_stat < obj_last_x[_id][0] and 1 <= _lane_id <= 99:
                            if lane_stat.get(_lane_id) is None:
                                lane_stat[_lane_id] = [0, 0, 0, 0, 0]
                            lane_stat[_lane_id][0] += 1
                            if delay_stat.get(_id) is not None:
                                lane_stat[_lane_id][1] += delay_stat[_id]
                            if stop_stat.get(_id) is not None:
                                lane_stat[_lane_id][2] += stop_stat[_id][0]

                            print('pass-obj-id:%6d, time:%6.2fs, delay:%6.2f, stop:%d  -->  lane_id:%4d' %
                                  (_id, (now-first_cycle_stat_time)/1e+6, delay_stat[_id] if delay_stat.get(_id) is not None else 0.,
                                   stop_stat[_id][0] if stop_stat.get(_id) is not None else 0., _lane_id))

                            used_lost_obj_ids = []
                            for lost_obj_id, lost_obj_info in lost_objs.items():
                                lo_rear_ids, lo_last_x, lo_last_time, lo_last_lane_id, lo_delay, lo_stop = lost_obj_info
                                if _id in lo_rear_ids and _lane_id == lo_last_lane_id:
                                    # lane_stat[_lane_id][0] += 1
                                    lane_stat[_lane_id][3] += lo_delay
                                    lane_stat[_lane_id][4] += lo_stop[0]
                                    used_lost_obj_ids.append(lost_obj_id)
                                    print('lost-obj-id:%6d, time:%6.2fs, delay:%6.2f, stop:%d  -->  lane_id:%4d by rear-obj-id:%6d at %6.2fs on %.2f' %
                                          (lost_obj_id, (lo_last_time - first_cycle_stat_time)/1e+6, lo_delay, lo_stop[0], lo_last_lane_id,
                                           _id, (now-first_cycle_stat_time)/1e+6, _x))
                            for used_lost_obj_id in used_lost_obj_ids:
                                lost_objs.pop(used_lost_obj_id)

                    if end_line_for_velocity <= _x <= start_line_for_velocity and 1 <= _lane_id <= 99:
                        if velocity_stat.get(_id) is None:
                            velocity_stat[_id] = [0., 0.]
                        velocity_stat[_id][0] += _speed
                        velocity_stat[_id][1] += 1.
                    if _x < end_line_for_velocity:
                        if velocity_stat.get(_id) is not None:
                            velocity_stat.pop(_id)

                    if 1 <= _lane_id <= 99:
                        obj_last_x[_id] = [_x, now, _lane_id]
                    else:
                        if obj_last_x.get(_id) is not None:
                            obj_last_x.pop(_id)

                x = abs(float((float(_x) - max_distance / 2) * scale_x) - float(edge / 2))
                y = -float(_y) * scale_y + float(edge / 2)
                if y < 0 or y > edge:
                    continue
                x, y = int(x), int(y)
                thickness = 1
                if -1 != _info.find('deleted;') \
                        or -1 != _info.find('be_merged;'):
                    cl = (160, 160, 160)
                    thickness = 2
                    if from_em:
                        remain_deleted.append([obj, 13])
                elif _rId == -1:
                    cl = (255, 0, 0)
                else:
                    if -1 != _info.find('new;'):
                        cl = (255, 0, 255)
                        # thickness = 3
                    elif -1 != _info.find('disable_merge;'):
                        cl = (0, 0, 255)
                    else:
                        cl = (0, 150, 0)

                if -1 != _info.find('new_merged;'):
                    thickness = 3
                if -1 != _info.find('!radian;'):
                    b_radian = True
                    # print("!radian:", _id)
                    cv2.putText(img, 'R', (y, x), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 1)

                if -1 == _info.find('deleted;'):
                    cv2.circle(img, (y, x), 8, cl, thickness)
                else:
                    cv2.line(img, (y - 6, x - 6), (y + 6, x + 6), cl, thickness)
                    cv2.line(img, (y + 6, x - 6), (y - 6, x + 6), cl, thickness)
                    if -1 != _info.find('in_blind_area;'):
                        cv2.rectangle(img, (y - 7, x - 7), (y + 7, x + 7), cl, 2)
                arrow(img, _orientation, y, x, 8, cl, 1)

                # info = '%d,%.2f' % (_id, _orientation)
                # info = '%d-%.1f' % (_id, _time_since_last_update)
                delay_seconds = 0
                if delay_stat.get(_id) is not None:
                    delay_seconds = delay_stat[_id]
                stop_count = 0
                if stop_stat.get(_id) is not None:
                    stop_count = stop_stat[_id][0]
                # info = '%d-%.1f-%d' % (_id, delay_seconds, stop_count)
                # info = '%d,%.2f,%.2f' % (_id, _x, _speed)
                if velocity_stat.get(_id) is None:
                    info = '%d,%.2f' % (_id, _speed)
                else:
                    vs = velocity_stat[_id]
                    info = '%d,%.2f,(%.2f)' % (_id, _speed, vs[0]/vs[1])
                cv2.putText(img, info, (y, x + 15), cv2.FONT_ITALIC, 0.36, (255, 0, 0), 1)

            remain_deleted = [[obj, n - 1] for obj, n in remain_deleted if n > 2]
            last_time = now
            if (now - last_cycle_stat_time) / 1e+6 >= 60.0 * 10.0:
                # print('cycle:%4d' % ((now - first_cycle_stat_time) / 1e+6))
                print('%10s,%4s,%5s,%10s,%10s,%10s,%10s,%10s,%10s,%10s,%10s'
                      % ('cycle', 'lane', 'count', 'sum_delay', 'sum_stop', 'avg_delay', 'avg_stop', 'sum_delay2', 'sum_stop2', 'avg_delay2', 'avg_stop2'))
                for ls in sorted(lane_stat.items(), key=lambda k: k[0]):
                    pass_obj_count, sum_delay, sum_stop, sum_delay2, sum_stop2 = ls[1]
                    sum_stop2 += sum_stop
                    sum_delay2 += sum_delay
                    avg_delay, avg_stop = 0., 0.
                    avg_delay2, avg_stop2 = 0., 0.
                    if pass_obj_count > 0:
                        avg_delay = sum_delay / pass_obj_count
                        avg_stop = sum_stop / pass_obj_count
                        avg_delay2 = sum_delay2 / pass_obj_count
                        avg_stop2 = sum_stop2 / pass_obj_count
                    print("CYCLE:%4d,%4d,%5d,%10.2f,%10.2f,%10.2f,%10.2f,%10.2f,%10.2f,%10.2f,%10.2f"
                          % (((now - first_cycle_stat_time) / 1e+6), ls[0], pass_obj_count, sum_delay, sum_stop, avg_delay, avg_stop, sum_delay2, sum_stop2, avg_delay2, avg_stop2))
                last_cycle_stat_time = now
                lane_stat.clear()

                print('%10s,%4s,%10s' % ('cycle', 'lane', 'length'))
                for lu in sorted(queue_stat.items(), key=lambda k: k[0]):
                    print("CYCLE:%4d,%4d,%10.2f" % (((now - first_cycle_stat_time) / 1e+6), lu[0], lu[1]))
                queue_stat.clear()

                print('%10s,%4s,%10s' % ('cycle', 'coil', 'count'))
                for cs in sorted(coil_stat.items(), key=lambda k: k[0]):
                    print("CYCLE:%4d,%4d,%10d" % (((now - first_cycle_stat_time) / 1e+6), cs[0], cs[1][2]))
                coil_stat.clear()

            _ids = list(obj_last_x.keys())
            for id in _ids:
                if id not in ids:
                    last_x, _last_time, last_lane_id = obj_last_x[id]
                    if last_x >= stop_line_for_stat:  # lost object
                        delay, stop = 0., 0
                        if delay_stat.get(id) is not None:
                            delay = delay_stat[id]
                        if stop_stat.get(id) is not None:
                            stop = stop_stat[id]
                        lost_objs[id] = [set(), last_x, _last_time, last_lane_id, delay, stop]
                    obj_last_x.pop(id)
            _ids = list(delay_stat.keys())
            for id in _ids:
                if id not in ids:
                    delay_stat.pop(id)
            _ids = list(stop_stat.keys())
            for id in _ids:
                if id not in ids:
                    stop_stat.pop(id)
            for _, lost_obj_info in lost_objs.items():
                lo_rear_ids = lost_obj_info[0]
                for lo_rear_id in list(lo_rear_ids):
                    if lo_rear_id not in ids:
                        lo_rear_ids.remove(lo_rear_id)

            last_frame_time = now


if __name__ == "__main__":
    pass

