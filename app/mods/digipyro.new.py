import cv2
import numpy as np

fps = 30
timeFinish = 5
timeStart = 0
x,y = 10,10
center = (x,y)
rpm = 10

fileName = 'check.mp4'
vid = cv2.VideoCapture(filename)
width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

fileName = 'checkRot'
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
video_writer = cv2.VideoWriter(fileName+'.mp4', fourcc, fps, (width, height))

numFrames = int(fps*(timeFinish - timeStart))

dtheta = 2*np.pi*rpm/(fps*60)
# dtheta = 6*rpm/fps

for i in range(numFrames):
    ret, frame = vid.read()
    frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)

    M = cv2.getRotationMatrix2D(center, i*dtheta, 1.0)
    frame = cv2.warpAffine(frame, M, (width, height))
    centered = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)
    video_writer.write(frame)

video_writer.release()
