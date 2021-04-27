import cv2
import numpy as np


def detect_circles(image):
    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('s', gray)
    cv2.waitKey(0)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1,15,param1 = 50,param2=9,minRadius=9,maxRadius=15)
    # ensure at least some circles were found
    if circles is not None:
        #print('%d circles detected',len(circles))
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        count = 0
        center_points = np.ndarray([])
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x, y), (x, y), (0, 128, 255), -1)
            count += 1
            center_points = np.append(center_points, [x, y])
        print(str(count) + ' circles detected.')

        # show the output image
        cv2.imshow("output", output)
        cv2.imwrite(r'C:\Users\Shane\Desktop\Year 3\Mathematical and Data Modelling\Phase C\LaurieOnTracking-master\circles.jpg',output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

path = r"C:\Users\Shane\Desktop\Year 3\Mathematical and Data Modelling\Phase C\LaurieOnTracking-master\FM_frames\frame0103.jpg"
detect_circles(cv2.imread(path))

