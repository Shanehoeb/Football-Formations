import matplotlib.pyplot as plt
import pandas
import ffmpeg
import numpy as np
import os
import cv2
import glob

# change location of writing and reading directory to write and read files and videos
path = r"C:\Users\Shane\Desktop\Year 3\Mathematical and Data Modelling\Phase C\LaurieOnTracking-master"
os.chdir(path)

vid = "\FM_test.avi"



def playvid(path=path, vid=vid):
    vidcap =cv2.VideoCapture(path+vid)
    framerate = vidcap.get(5)
    framecount = vidcap.get(7)
#     print(framerate, framecount)
    while True:
        success, frame = vidcap.read()
        if success:
            cv2.imshow('frame',frame)
            cv2.waitKey(1)
        else:
            break

    vidcap.release()
    cv2.destroyAllWindows()

    


def framesplit(path=path, vid=vid):
    #Add extension to path to store images in a separate folder
    extension = '\FM_frames'
    os.chdir(path+extension)
    vidcap =cv2.VideoCapture(path+vid)
    framerate = vidcap.get(5)
    framecount = vidcap.get(7)
    print(framerate, framecount)
    count = 0
    success, frame = vidcap.read()
    print(success)
    while success: 
        cv2.imwrite("frame%s.jpg" % str(count).zfill(3), frame)     # save frame as JPEG file      
        success,frame = vidcap.read()
        #print('Read a new frame: ', success)
        count += 1
    vidcap.release()
    
 

def makevideo(vid=vid):
    img_array = []
    #path to frame file
    frame_file_path = r'C:\Users\Shane\Desktop\Year 3\Mathematical and Data Modelling\Phase C\LaurieOnTracking-master\FM_Frames\*.jpg'
    for filename in glob.glob(frame_file_path):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
   
    out = cv2.VideoWriter(r'C:\Users\Shane\Desktop\Year 3\Mathematical and Data Modelling\Phase C\LaurieOnTracking-master\test_vid.avi',cv2.VideoWriter_fourcc(*'DIVX'), 60, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

framesplit()
makevideo(vid)
