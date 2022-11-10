import sys
import time
import math
import cv2
import numpy as np
import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber


scale = 800./600.
edge = int(600 * scale)
max_distance = 300
scale_y = 20.0 * scale
scale_x = math.floor(edge / max_distance)
scale_y = scale_x * 6


def translate_x(_x):
    return abs(float((float(_x) - max_distance / 2) * scale_x) - float(edge / 2))


def translate_y(_y):
    return -float(_y) * scale_y + float(edge / 2)


def main(azimuth540, elevation540, min_velocity):
    print("eCAL {} ({})\n".format(ecal_core.getversion(), ecal_core.getdate()))
    ecal_core.initialize(sys.argv, "cluster_receive")
    ecal_core.set_process_state(1, 1, "I feel good")
    sub540 = StringSubscriber("Txt079")

    duration_seconds = 0

    meas_line = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 200]
    meas_line = np.array(meas_line)[np.where(np.array(meas_line) <= max_distance)]
    lane_line = [9, 6, 3, 0, -3, -6, -9]

    # img_template
    img_tpl = np.ones((edge, edge, 3), np.uint8)
    img_tpl *= 255

    cv2.circle(img_tpl, (int(translate_y(0)), int(translate_x(0))), 3, (255, 0, 0), thickness=5)
    for ll in lane_line:
        _ll = ll
        ll = int(translate_y(ll))
        cv2.line(img_tpl, (ll, 0), (ll, edge), (196, 228, 255))
        cv2.putText(img_tpl, '%d' % _ll, (ll, edge - 30), cv2.FONT_ITALIC, 0.4, (0, 0, 0), 1)
    for ml in meas_line:
        _ml = ml
        ml = int(translate_x(ml))
        cv2.line(img_tpl, (0, ml), (edge, ml), (255, 255, 0))
        cv2.putText(img_tpl, '%03d' % _ml, (10, ml), cv2.FONT_ITALIC, 0.4, (0, 0, 0), 1)

    img = np.copy(img_tpl)

    no = 0
    i = 0
    model_no = -1
    while ecal_core.ok():
        i += 1
        if model_no == 540:
            model_no = -1
            no += 1

            cv2.putText(img, 'azimuth540: %.4f' % azimuth540,   (edge - 190, 50), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1)
            cv2.putText(img, 'elevation5: %.4f' % elevation540, (edge - 190, 80), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1)
            cv2.putText(img, '%d' % no, (edge - 160, 80), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 0, 0), 1)
            cv2.putText(img, '%02d:%02d' % (duration_seconds / 60, duration_seconds % 60), (5, 80), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 1)

            cv2.imshow('cs&540', img)

            key = cv2.waitKeyEx(1)
            if key == 27:  # Esc
                ecal_core.finalize()
                exit(0)
            elif key == 43:  # +
                # azimuth540 += 0.01
                elevation540 += 0.01
            elif key == 45:  # -
                # azimuth540 -= 0.01
                elevation540 -= 0.01
            elif key == 2490368:  # move up
                # azimuth540 += 0.001
                elevation540 += 0.001
            elif key == 2621440:  # move down
                # azimuth540 -= 0.001
                elevation540 -= 0.001
            elif key == 2555904:  # ->(move right)
                pass
            elif key == 2424832:  # <-(move left)
                pass
            if key != -1:
                print('key:%d' % key)

            i = 0
            img = np.copy(img_tpl)

        count540 = 0
        _, msg, _ = sub540.receive()
        if msg == '':
            continue
        model_no = 540
        lines = msg.split('\n')
        for line in lines:
            items = line.split(',')
            if len(items) == 13:
                _id, x, y, z, vx, vy, prop, rcs, measState, poe, _l, _w, class_type = items
                if float(x) > max_distance:
                    continue
                measState = int(measState)

                count540 += 1
                _rcs = rcs
                _x, _y = x, y
                vx, vy = float(vx), float(vy)
                _vx, _vy = vx, vy
                vx = math.cos(azimuth540) * _vx - math.sin(azimuth540) * _vy
                vy = math.cos(azimuth540) * _vy + math.sin(azimuth540) * _vx
                if not (abs(vx) >= min_velocity or abs(vy) >= min_velocity):
                    continue

                xs, ys = float(x), float(y)
                x = math.cos(azimuth540) * xs - math.sin(azimuth540) * ys
                y = math.cos(azimuth540) * ys + math.sin(azimuth540) * xs
                z = float(z)
                z = math.cos(elevation540) * z + math.sin(elevation540) * x
                '''
                if x < 10 and abs(y) < 1:
                    print('xyz: %10.6f, %10.6f, %10.6f' % (x, y, z))
                else:
                    continue
                '''

                x = translate_x(x)
                y = translate_y(-y)
                if y < 0 or y > edge:
                    continue

                x, y = int(x), int(y)
                prop = int(prop)
                rcs = int(rcs)

                r = g = b = 0
                if measState == 3:  # predicted
                    r = 255
                cv2.circle(img, (y, x), 5, (b, g, r), thickness=1)

                # info = ' %s,%s' % (_id, z)
                info = ' %.2f' % z
                # info = ' %.2f, %.2f, %.2f' % (xs, ys, z)
                cv2.putText(img, info, (y, x-1), cv2.FONT_ITALIC, 0.4, (b, g, r), 1)

                _l = float(_l)*5
                _w = float(_w)*5
                cv2.line(img, (y, int(x - _l/2)), (y, int(x + _l/2)), (b, g, r))
                cv2.line(img, (int(y - _w/2), x), (int(y + _w/2), x), (b, g, r))

        cv2.putText(img, '%d' % count540, (edge - 160, 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 1)


if __name__ == "__main__":
    _azimuth540 = 0.0
    _elevation540 = -0.022
    _min_velocity = 0.25
    for i in range(len(sys.argv)):
        if sys.argv[i] == '--azimuth540' and len(sys.argv) > i+1:
            _azimuth540 = float(sys.argv[i+1])
        elif sys.argv[i] == '--velocity' and len(sys.argv) > i+1:
            _min_velocity = float(sys.argv[i+1])

    main(_azimuth540, _elevation540, _min_velocity)

