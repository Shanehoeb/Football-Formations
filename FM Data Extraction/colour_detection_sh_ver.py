import cv2
import os
import imutils
import numpy as np
from scipy.spatial import Delaunay
from scipy.spatial import Voronoi, voronoi_plot_2d
# Python code for Multiple Color Detection
import pandas as pd


def draw_lines_between_players(img, team, colour, thickness):
	if np.shape(team)[0] > 1:
		for i in range(np.shape(team)[0]-1):
			for j in range(i, np.shape(team)[0]):
				cv2.line(img, (team[i][0], team[i][1]), (team[j][0], team[j][1]), colour, thickness)
	return


def draw_delaunay(img,team,colour,thickness):
	if np.shape(team)[0] > 2:
		lines = Delaunay(team)
		for count in range(len(lines.simplices)):
				point1 = tuple(team[lines.simplices[count][0]])
				point2 = tuple(team[lines.simplices[count][1]])
				point3 = tuple(team[lines.simplices[count][2]])
				cv2.line(img, point1, point2, colour, thickness)
				cv2.line(img, point1, point3, colour, thickness)
				cv2.line(img, point3, point2, colour, thickness)


def draw_voronoi(img, team1, team2, colour, thickness):
	if np.shape(team1)[0] > 2 and np.shape(team2)[0] > 2:
		for i in range(len(team1)):
				team2.append(team1[i])
		vor = Voronoi(white_team)
		i = 0
		#vertices
		while i < len(vor.vertices)-1:
			point1 = (int(vor.vertices[i][0]), int(vor.vertices[i][1]))
			point2 = (int(vor.vertices[i+1][0]), int(vor.vertices[i+1][1]))
			cv2.line(img, point1, point2, colour, thickness)
			i += 1
		i = 0
		while i < len(vor.vor.ridge_vertices)-1:
			point1 = (int(vor.vor.ridge_vertices[i][0]), int(vor.vor.ridge_vertices[i][1]))
			point2 = (int(vor.vor.ridge_vertices[i+1][0]), int(vor.vor.ridge_vertices[i+1][1]))
			cv2.line(img, point1, point2, colour, thickness)
			i+=1
		pass

def format_data(list,frame_number):
	x_list = []
	y_list = []
	frame_list = []
	for element in list:
		x_list.append(element[0])
		y_list.append(element[1])
		frame_list.append(frame_number)
	return x_list,y_list, frame_list


def plot_circle(mask, colour, colour_tuple, max_radius, frame, size):
	contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	team = []
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if 0 < area < 300:
			x, y, w, h = cv2.boundingRect(contour)
			((X, Y), radius) = cv2.minEnclosingCircle(contour)
			M = cv2.moments(contour)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			if radius < max_radius:
				frame = cv2.circle(frame, (int(X), int(Y)), int(radius), colour_tuple, size)
				cv2.putText(frame, colour, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, colour_tuple)
				team.append([x, y])
	return team

def plot_rectangle(mask, colour, colour_tuple, max_wh, frame):
	contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	team = []
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if area > 300:
			x, y, w, h = cv2.boundingRect(contour)
			if h >= 1.5 * w:
				if w > max_wh and h >= max_wh:
					imageFrame = cv2.rectangle(frame, (x, y), (x + w, y + h), colour_tuple, 2)
					team.append([x, y])
					cv2.putText(frame, colour, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, colour_tuple)
	return team


def transform_list(list):
	x = []
	for i in range(0, len(list)):
		for element in list[i]:
			x.append(element)
	return x


# Set range for color and
# define mask
red_lower = np.array([136, 87, 111], np.uint8)
red_upper = np.array([180, 255, 255], np.uint8)

blue_lower = np.array([94, 80, 2], np.uint8)
blue_upper = np.array([120, 255, 255], np.uint8)

lower_white = np.array([0,0,200], np.uint8)
upper_white = np.array([145, 60, 255], np.uint8)

lower_yellow = np.array([22, 93, 0])
upper_yellow = np.array([45, 255, 255])


# Capturing video through webcam
webcam = cv2.VideoCapture(r"C:\Users\Shane\Downloads\Vid3.mp4")
a = webcam.get(cv2.CAP_PROP_FPS)
image, success = webcam.read()

i = 0
x = []
y = []
frame = []
# Start a while loop
while i < 500:

	# Reading the video from the
	# webcam in image frames
	_, imageFrame = webcam.read()
	imageFrame = imutils.resize(imageFrame, width=800)

	# Convert the imageFrame in
	# BGR(RGB color space) to
	# HSV(hue-saturation-value)
	# color space
	hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

	red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
	blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
	white_mask = cv2.inRange(hsvFrame, lower_white, upper_white)


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

	red_team = plot_circle(red_mask, 'red', (0, 0, 255), 10, imageFrame, 2)
	white_team = plot_circle(blue_mask, 'blue', (255, 0, 0), 10, imageFrame, 2)

	#ball_pos = plot_circle(white_mask, 'ball', (0, 255, 0), 2, imageFrame, 2)
	draw_delaunay(imageFrame, red_team, (0, 0, 255), 3)
	draw_delaunay(imageFrame, white_team, (0, 255, 0), 3)
	#draw_voronoi(imageFrame,red_team,white_team, (0, 255, 0), 3)
	x_h,y_h,frame_h = format_data(white_team, i)
	x.append(x_h)
	y.append(y_h)
	frame.append(frame_h)
	i +=1

	cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	success, image = webcam.read()
webcam.release()
cv2.destroyAllWindows()


x = transform_list(x)
y = transform_list(y)
frame = transform_list(frame)

df = pd.DataFrame({"x_coor":x, "y_coor":y, "frame":frame})
path_to_csv = r'C:\Users\Shane\Desktop\Year 3\Mathematical and Data Modelling\Phase C\LaurieOnTracking-master\file.csv'
df.to_csv(path_to_csv)

