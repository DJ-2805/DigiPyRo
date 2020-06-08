import cv2
import numpy as np

fps = 30
timeFinish = 5
timeStart = 0
x,y = 10,10
center = (x,y)
rpm = 10



fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
video_writer = cv2.VideoWriter(fileName+'.mp4', fourcc, fps, )

numFrames = int(fps*(timeFinish - timeStart))

dtheta = 2*np.pi*rpm/(fps*60)
# dtheta = 6*rpm/fps

for i in range(numFrames):
    M = cv2.getRotationMatrix2D(center, i*dtheta, 1.0)
