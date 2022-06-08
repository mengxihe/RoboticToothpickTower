import cv2
import socket
import numpy as np


def UDP_client(IP, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(message, "utf-8"), (IP, port))
font = cv2.FONT_HERSHEY_COMPLEX
IP = "192.168.0.106" #141.58.222.34
port = 5000
img2 = cv2.imread('opencv_frame_35.png', cv2.IMREAD_COLOR)
img = cv2.imread('opencv_frame_35.png', cv2.IMREAD_GRAYSCALE)
_, threshold = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE,
                               cv2.CHAIN_APPROX_SIMPLE)
yList = []
xList = []
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
    area = cv2.contourArea(cnt)
    if area > 5000:
        cv2.drawContours(img2, [approx], -1, (0, 0, 255), 2)
        # Used to flatted the array containing
        # the co-ordinates of the vertices.
        n = approx.ravel()
        i = 0
        for j in n:
            if i % 2 == 0:
                x = n[i]
                y = n[i + 1]
                string = str(x) + " " + str(y)
                if (i == 0):
                    # text on topmost co-ordinate.
                    cv2.putText(img2, "Arrow tip", (x, y),
                                font, 0.5, (255, 0, 0))
                else:
                    # text on remaining co-ordinates.
                    cv2.putText(img2, string, (x, y),
                                font, 0.5, (0, 255, 0))
                xList.append(x)
                yList.append(y)
            i = i + 1
message = "{}, {}".format(xList, yList)
UDP_client(IP, port, message)
img3 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
stacked = np.concatenate((img3, img2), axis=1)
#cv2.imshow('opencv_frame_20.png', stacked)
k = cv2.waitKey(1)
#cv2.imwrite('opencv_frame_35.png', stacked)
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()