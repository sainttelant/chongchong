import socket
import cv2
import numpy as np
import time


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 本机的ip地址
address = ("10.203.204.155", 9050)
server_socket.bind(address)
server_socket.settimeout(0.3)


def main():
    h, w = 560, 800
    img = np.ones((h, w, 3), np.uint8)
    img *= 255
    y_start = 80
    y_step = 3

    coil_x = {}
    coil_y = {}
    coil_pulse_count = {}
    coil_pulse_state = {}
    for i in range(36):
        coil_x[i+1] = (i+1) * 15
        coil_y[i+1] = y_start
        coil_pulse_state[i+1] = 0
        coil_pulse_count[i+1] = 0
    for n, x in coil_x.items():
        cv2.putText(img, '%2d' % n, (0, x), cv2.FONT_ITALIC, 0.4, (0, 0, 0), 1)

    last_time = time.time()
    while True:
        cv2.imshow('pulse', img)
        key = cv2.waitKey(1)
        if key == 27:  # Esc
            exit(0)

        try:
            msg, client = server_socket.recvfrom(10240)
            current = time.time()
            cycle = int((current - last_time) * 100)  # 10ms
            last_time = current
        except socket.timeout:
            continue

        if len(msg) == 13 and msg[3] == 0x10 and msg[4] == 0x82 and msg[5] == 0x88:
            link_address = msg[1]
            link_num = msg[2]
            pulse_1_8   = bin(msg[7])[2:]
            pulse_9_16  = bin(msg[8])[2:]
            pulse_1_8   = ('%08s' % pulse_1_8 ).replace(' ', '0')[::-1]
            pulse_9_16  = ('%08s' % pulse_9_16).replace(' ', '0')[::-1]
            pulse = ('%s%s' % (pulse_1_8, pulse_9_16))[:link_num]
            # print('%d, %d, %s, %d' % (link_address, link_num, pulse, cycle))
            for i, c in enumerate(list(pulse)):
                coil_key = link_address + i + 1
                y = coil_y.get(coil_key)
                x = coil_x.get(coil_key)
                if not y or not x:
                    continue

                if '1' == c:
                    cl = (0, 0, 255)
                    if coil_pulse_state[coil_key] == 0:
                        coil_pulse_state[coil_key] = 1
                else:
                    cl = (0, 255, 0)
                    if coil_pulse_state[coil_key] == 1:
                        coil_pulse_state[coil_key] = 0
                        coil_pulse_count[coil_key] += 1
                cv2.line(img, (y, x-10), (y, x-1), cl, lineType=cv2.LINE_8, thickness=2)
                if i == 0:
                    if link_address > 0:
                        cv2.line(img, (0, x - 13), (w, x - 13), (255, 0, 0), lineType=cv2.LINE_8, thickness=2)
                    # cv2.circle(img, (y, x-cycle), 1, (0, 0, 0), thickness=1)
                elif i % 3 == 0:
                    cv2.line(img, (0, x - 12), (w, x - 12), (0, 255, 0), lineType=cv2.LINE_8, thickness=1)

                img[x-10: x+1, 18:y_start] = (np.ones((11, y_start-18, 3), np.uint8) * 255)
                cv2.putText(img, '%3d' % coil_pulse_count[coil_key], (30, x), cv2.FONT_ITALIC, 0.4, (0, 0, 0), 1)

                coil_y[coil_key] += y_step
                if coil_y[coil_key] >= w - y_step:
                    img[x-10:x, y_start:-3] = img[x-10:x, y_start + 3:]
                    img[x-10:x, -3:] = (np.ones((10, 3, 3), np.uint8) * 255)
                    coil_y[coil_key] -= y_step


if __name__ == "__main__":
    main()

