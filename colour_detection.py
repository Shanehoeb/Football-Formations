import cv2
import os
import numpy as np

# Python code for Multiple Color Detection

def draw_lines_between_players(img, team, colour, thickness):
	if np.shape(team)[0] > 1:
		for i in range(np.shape(team)[0]-1):
			cv2.line(img, (team[i][0], team[i][1]), (team[i+1][0], team[i+1][1]), colour, thickness)
	return


# Capturing video through webcam
webcam = cv2.VideoCapture(0)
webcam = cv2.VideoCapture('football_manager_Trim.mp4')
image, success = webcam.read()

# Start a while loop
while 1:

	# Reading the video from the
	# webcam in image frames
	_, imageFrame = webcam.read()

	# Convert the imageFrame in
	# BGR(RGB color space) to
	# HSV(hue-saturation-value)
	# color space
	hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

	# Set range for red color and
	# define mask
	red_lower = np.array([136, 87, 111], np.uint8)
	red_upper = np.array([180, 255, 255], np.uint8)
	red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

	# Set range for blue color and
	# define mask
	blue_lower = np.array([94, 80, 2], np.uint8)
	blue_upper = np.array([120, 255, 255], np.uint8)
	blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)


	lower_white = np.array([0,0,200], np.uint8)
	upper_white = np.array([145,60,255], np.uint8)
	white_mask = cv2.inRange(hsvFrame, lower_white, upper_white)

	lower_yellow = np.array([22, 93, 0])
	upper_yellow = np.array([45, 255, 255])
	# Morphological Transform, Dilation
	# for each color and bitwise_and operator
	# between imageFrame and mask determines
	# to detect only that particular color
	kernal = np.ones((5, 5), "uint8")

	# For red color
	red_mask = cv2.dilate(red_mask, kernal)
	res_red = cv2.bitwise_and(imageFrame, imageFrame, mask=red_mask)

	# For blue color
	blue_mask = cv2.dilate(blue_mask, kernal)
	res_blue = cv2.bitwise_and(imageFrame, imageFrame, mask=blue_mask)

	# Creating contour to track red color
	contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	team1 = []
	team2 = []
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if 0 < area < 300:
			x, y, w, h = cv2.boundingRect(contour)
			((X, Y), radius) = cv2.minEnclosingCircle(contour)
			M = cv2.moments(contour)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			if radius < 10:
				imageFrame = cv2.circle(imageFrame, (int(X), int(Y)), int(radius), (0, 0, 255), 2)
				#team1.append([x, y])
				cv2.putText(imageFrame, "Red", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255))
		#draw_lines_between_players(imageFrame, team1, (0,0,255), 3)


	contours, heirachy = cv2.findContours(white_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if 0 < area < 300:
			x, y, w, h = cv2.boundingRect(contour)
			((X, Y), radius) = cv2.minEnclosingCircle(contour)
			M = cv2.moments(contour)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			if radius < 10:
				if radius < 2:
					imageFrame = cv2.circle(imageFrame, (int(X), int(Y)), int(radius), (0, 255, 0), 2)
				#team2.append([x, y])
					cv2.putText(imageFrame, "Ball", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0))
				else:
					imageFrame = cv2.circle(imageFrame, (int(X), int(Y)), int(radius), (255, 255, 255), 2)
					cv2.putText(imageFrame, "White", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255))

		#draw_lines_between_players(imageFrame, team2, (0,255,0), 3)

	cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	success, image = webcam.read()
webcam.release()
cv2.destroyAllWindows()
