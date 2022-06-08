import cv2

cap = cv2.VideoCapture(0)

cv2.namedWindow("Screenshot App")

img_counter = 0

while True:
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

cap.release()

cv2.destroyAllWindows()
