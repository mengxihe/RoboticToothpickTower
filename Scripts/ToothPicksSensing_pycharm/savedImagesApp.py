import cv2
import numpy as np
import socket
import time
import math


font = cv2.FONT_HERSHEY_COMPLEX
# A required callback method that goes into the trackbar function.
def nothing(x):
    pass

# Initializing the webcam feed
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

cv2.namedWindow("Trackbars")

# Now create 6 trackbars that will control the lower and upper range of
# H,S and V channels. The Arguments are like this: Name of trackbar,
# window name, range,callback function. For Hue the range is 0-179 and
# for S,V its 0-255.
cv2.createTrackbar("L - H", "Trackbars", 91, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 29, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 197, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 148, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 101, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

img_counter = 0

while True:
    # take shoots from videocam
    ret, frame = cap.read()

    if ret:
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    if not ret:
        print("failed to grab frame")
        break
    frame = cv2.flip(frame, 1)
    # blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get the new values of the trackbar in real time as the user changes
    # them
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    # Set the lower and upper HSV range according to the value selected
    # by the trackbar
    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])

    # Filter the image and get the binary mask, where white represents
    # your target color
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # You can also visualize the real part of the target color (Optional)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Converting the binary mask to 3 channel image, this is just so
    # we can stack it with the others
    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # stack the mask, orginal frame and the filtered result
    stacked = np.hstack((mask_3, res))

    #cv2.imshow("Screenshot App", frame)
    cv2.imshow("Frame", cv2.resize(frame, None, fx=0.4, fy=0.4))
    # cv2.imshow("Mask", mask)
    # Show this stacked frame at 40% of the size.
    cv2.imshow('Trackbars', cv2.resize(stacked, None, fx=0.3, fy=0.3))

    k = cv2.waitKey(1)
    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

    elif k % 256 ==32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, mask)
        print("{} written!".format(img_name))
        img_counter += 1

        # readImage

        img2 = cv2.imread(img_name, cv2.IMREAD_COLOR)
        # Reading same image in another
        # variable and converting to gray scale.
        img = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)

        # Converting image to a binary image
        # ( black and white only image).
        _, threshold = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)

        # Detecting contours in image.
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
        # print(contours)
        # Going through every contours found in the image.
        yList = []
        xList = []

        for cnt in contours:

            approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
            area = cv2.contourArea(cnt)
            # print(approx)
            # draws boundary of contours

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

                        # string containing the co-ordinates
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

                    i = i+1
        print(xList)
        cv2.imshow('image2', cv2.resize(img2, None, fx=0.4, fy=0.4))

cap.release()

cv2.destroyAllWindows()