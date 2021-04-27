#Import libraries
import cv2
import os
import numpy as np


def draw_lines_between_players(img, team, colour, thickness):
	if np.shape(team)[0] > 1:
		for i in range(np.shape(team)[0]-1):
			cv2.line(img, (team[i][0], team[i][1]), (team[i+1][0], team[i+1][1]), colour, thickness)
	return


vidcap = cv2.VideoCapture('red_vs_blue.mp4')
success,image = vidcap.read()
count = 0
success = True
idx = 0

while success:
	hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

	lower_green = np.array([40,40, 40])
	upper_green = np.array([70, 255, 255])
	#blue range
	lower_blue = np.array([110,150,0], np.uint8)
	upper_blue = np.array([140,255,255], np.uint8)

	#Red range
	upper_red = np.array([180, 255, 255], np.uint8)
	lower_red = np.array([136, 87, 111], np.uint8)

	#white range
	lower_white = np.array([0,0,0])
	upper_white = np.array([0,0,255])

	#Define a mask ranging from lower to uppper
	mask = cv2.inRange(hsv, lower_green, upper_green)
	#Do masking
	res = cv2.bitwise_and(image, image, mask=mask)
	#convert to hsv to gray
	res_bgr = cv2.cvtColor(res,cv2.COLOR_HSV2BGR)
	res_gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

	#Defining a kernel to do morphological operation in threshold image to
	#get better output.
	kernel = np.ones((13,13),np.uint8)
	thresh = cv2.threshold(res_gray,0,500,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

	#find contours in threshold image
	contours, heirachy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#find contours in threshold image

	prev = 0
	font = cv2.FONT_HERSHEY_SIMPLEX
	team1 = []
	team2 = []
	for c in contours:
		x,y,w,h = cv2.boundingRect(c)

		#Detect players
		if(h>=(1.5)*w):
			if(h>=15 and w>=15):
				player_img = image[y:y+h,x:x+w]

				player_hsv = cv2.cvtColor(player_img,cv2.COLOR_BGR2HSV)
				#white ball  detection
				mask1 = cv2.inRange(player_hsv, lower_blue, upper_blue)
				mask1 = cv2.dilate(mask1, kernel)
				res1 = cv2.bitwise_and(player_img, player_img, mask=mask1)
				res1 = cv2.cvtColor(res1,cv2.COLOR_HSV2BGR)
				res1 = cv2.cvtColor(res1,cv2.COLOR_BGR2GRAY)
				nzCountred = cv2.countNonZero(res1)
				mask2 = cv2.inRange(player_hsv, lower_red, upper_red)
				mask2 = cv2.dilate(mask2, kernel)
				res2 = cv2.bitwise_and(player_img, player_img, mask=mask2)
				res2 = cv2.cvtColor(res2,cv2.COLOR_HSV2BGR)
				res2 = cv2.cvtColor(res2,cv2.COLOR_BGR2GRAY)
				nzCountblue = cv2.countNonZero(res2)



				if(nzCountred > 0):
					# detect football
					cv2.putText(image, 'blue', (x-2, y-2), font, 0.8, (110,50,50), 2, cv2.LINE_AA)
					cv2.rectangle(image,(x,y),(x+w,y+h),(110,50,50),3)
					team1.append([x, y])
					draw_lines_between_players(image, team1, (110,50,50), 3)

				if(nzCountblue > 0):
					# detect football
					cv2.putText(image, 'red', (x-2, y-2), font, 0.8, (0,31,255), 2, cv2.LINE_AA)
					cv2.rectangle(image,(x,y),(x+w,y+h),(0,31,255),3)
					team2.append([x, y])
					draw_lines_between_players(image, team2, (0,31,255), 3)


	cv2.imwrite("./Cropped/frame%d.jpg", res)     # save frame as JPEG file
	cv2.imshow('Match Detection',image)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	success,image = vidcap.read()

vidcap.release()
cv2.destroyAllWindows()
