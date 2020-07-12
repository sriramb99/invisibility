import numpy as np
import cv2
import time

capture_video = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = capture_video.read()
    # Allowing the camera to warm up
    time.sleep(1)
    count = 0
    background = 0

    # Capturing the background in range of 60
    for i in range(60):
        return_val, background = capture_video.read()
        if return_val == False:
            continue

    background = np.flip(background, axis=1)

    # We will be reading from the live video from the webcam
    while (capture_video.isOpened()):
        return_val, img = capture_video.read()
        if not return_val:
            break
        count = count + 1
        img = np.flip(img, axis=1)
        # Convert the image from BGR to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Generating a mask to detect the red color
        # HSV
        # It should be a mono-color cloth for full invisibility

        lower_red = np.array([100, 40, 40])
        upper_red = np.array([100, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        lower_red = np.array([155, 40, 40])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red, upper_red)

        mask1 = mask1 + mask2

        # Refining the mask corresponding to the detected red color
        mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
        mask1 = cv2.dilate(mask1, np.ones((3, 3), np.uint8), iterations=1)
        mask2 = cv2.bitwise_not(mask1)

        # Generating the final output
        res1 = cv2.bitwise_and(background, background, mask=mask1)
        res2 = cv2.bitwise_and(img, img, mask=mask2)
        final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

        cv2.imshow("Disappear", final_output)
        k = cv2.waitKey(10)
        if k == 27:
            break

# When everything is done, release the capture
capture_video.release()
cv2.destroyAllWindows()

