import cv2
import numpy
import socket


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

cv2.namedWindow("Screenshot App")


img_counter = 0
while True:
    # take shoots from videocam
    ret, frame = cap.read()

    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("Screenshot App", frame)

    k = cv2.waitKey(1)
    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

    elif k % 256 ==32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

        # readImage
        font = cv2.FONT_HERSHEY_COMPLEX
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
        nList = []
        xList = []

        for cnt in contours:

            approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
            # print(approx)
            # draws boundary of contours
            cv2.drawContours(img2, [approx], 0, (0, 0, 255), 5)
            # Used to flatted the array containing
            # the co-ordinates of the vertices.
            n = approx.ravel()
            i = 0
            nList.append(n)

            for j in n:
                if (i % 2 == 0):
                    x = n[i]
                    y = n[i + 1]

                    # string containing the co-ordinates
                    string = str(x) + " " + str(y)

                    cv2.putText(img2, string, (x, y),
                                font, 0.5, (0, 255, 0))

                    xList.append(x)

                i = i+1
        print(xList)
        cv2.imshow('image2', img2)

cap.release()

cv2.destroyAllWindows()