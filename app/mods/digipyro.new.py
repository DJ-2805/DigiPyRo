import argparse

import cv2
import numpy as np

import interaction as interact
#------------------------------------------------------------------------------
# *** COMMAND LINE INTERFACE SETUP ***
# initial message for program
msg = """ This program digitally rotates a movie. It can take a video from
the synthetic program as well as other movies to rotate and place the user in
the rotating frame. The user may input several variables and will need to
select an area of interest, so the program rotates about the correct axis."""
fmt = argparse.ArgumentDefaultsHelpFormatter
parser = argparse.ArgumentParser(description=msg,
                                 formatter_class=fmt)

# collecting arguments for the user to change
parser.add_argument('--t0', type=float, default=0,
                    help='The start time for the digital rotation.')

parser.add_argument('--t1', type=float, default=5,
                    help='The end time for the digital rotation.')

parser.add_argument('--rpm', type=float, default=10,
                   help='The digital rotation given to the movie.')

parser.add_argument('--path', type=str, default='../../../movie',
                    help='The complete path of the movie being inputted.')
#------------------------------------------------------------------------------

# collecting user input into list
args = parser.parse_args()

fps = 30

t0 = args.t0
t1 = args.t1
rpm = args.rpm
path = args.path

def digi_rotate(t0, t1, rpm, path):
    fps = 30

    vid = cv2.VideoCapture(path + '.mp4')
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    dim = (width, height)

    start = fps * t0
    if start == 0:
        start = 1

    output = path + '-rot.mp4'
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video_writer = cv2.VideoWriter(output, fourcc, fps, dim)

    poly1, poly2, center = interact.selection_window(vid, dim, start)

    frames = int(fps * (t1 - t0))
    dtheta = 6 * rpm / fps
    for i in range(frames):
        ret, frame = vid.read()
        frame = cv2.resize(frame, dim, interpolation=cv2.INTER_CUBIC)

        cv2.fillPoly(frame, np.array([poly1, poly2]), 0)
        cv2.circle(frame, center, 4, (255,0,0), -1)

        M = cv2.getRotationMatrix2D(center, i*dtheta, 1.0)
        frame = cv2.warpAffine(frame, M, dim)

        frame = interact.center_frame(frame, center[0], center[1], dim)
        centered = cv2.resize(frame, dim, interpolation=cv2.INTER_CUBIC)
        video_writer.write(centered)

    video_writer.release()

if __name__ == "__main__":
    digi_rotate(t0, t1, rpm, path)
