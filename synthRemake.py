# libraries
import argparse as ap             # terminal flags
import numpy as np                # numerical lib
import cv2                        # opencv lib
import matplotlib                 # figure lib
import matplotlib.pyplot as plt   # plotting lib

matplotlib.use("Agg")

#------------------------------------------------------------------------------
# *** COMMAND LINE INTERFACE SETUP ***
# initial message for program
msg = 'This program creates a synthetic .avi movie for use with DigiPyRo. '
msg += 'The video shows a ball rolling on a parabolic surface. '
msg += 'The user may change the length of the movie, the frame rate, the resolution of the movie, the frequency of oscillations, '
msg += 'the rotation rate of the reference frame, and control the initial conditions of the ball.'
parser = ap.ArgumentParser(description = msg,
                           formatter_class=ap.ArgumentDefaultsHelpFormatter)

# collecting arguments for the user to change
parser.add_argument('-t', '--time', type=float, default=5,
                    help='The desired length of the movie in seconds.')
parser.add_argument('-f', '--fps', type=float, default=30.0,
                    help=('The frame rate of the video (frames per second). '
                          'Set this to a low value (10-15) for increased speed'
                          ' or a higher value (30-60) for better results.'))
parser.add_argument('--width', type=int, default=1260,
                    help=('The width in pixels of the video. '
                          'Decrease the width and height for increased '
                          'speed or increase these values for '
                          'improved resolution.'))
parser.add_argument('--height', type=int, default=720,
                    help='The height in pixels of the video.')
parser.add_argument('-r', '--eqpot_rpm', type=float, default=10.0,
                    help=('The deflection of a stationary paraboloid surface '
                          'as if it were an equipotentional in a system '
                          'rotating at the specified rate. '
                          'A good value would be between 5 and 15.'))
parser.add_argument('-R', '--cam_rpm', type=float, default=0.0,
                    help=('The rotation rate of the camera. The two natural '
                          'frames of reference are with cam_rpm = 0 or '
                          'cam_rpm = rpm.'))
parser.add_argument('--r0', type=float, default=1.0,
                    help=('The initial radial position of the ball. Choose a '
                          'value betweeon 0 and 1.'))
parser.add_argument('--vr0', type=float, default=0.0,
                    help=('The initial radial velocity of the ball. '
                          'A good value would be between 0 and 1.'))
parser.add_argument('--phi0', type=float, default=np.pi/4,
                    help=('The initial azimuthal position of the ball. '
                          'Choose a value between 0 and 2*pi.'))
parser.add_argument('--vphi0', type=float, default = 0,
                    help=('The initial azimuthal velocity of the ball. '
                          'A good value would be between 0 and 1.'))

# collecting user input into list
args = parser.parse_args()

#-----------------------------------------------------------------------------

if __name__ == "__main__":
    # spinlab logo to display in upper right corner of output video
    spinlab = cv2.imread('util/SpinLabUCLA_BW_strokes.png')

    # Define movie details
    movLength = args.time
    fps = args.fps
    width = args.width
    height = args.height
    spinlab = cv2.resize(spinlab,(int(0.2*width),int((0.2*height)/3)), interpolation = cv2.INTER_CUBIC)

    # Define table value
    # NOTE: A two-dimensional rotating system naturally takes the shape of a parabola.
    # The rotation rate determines the curvature of the parabola, which is why we define the curvature in terms of RPM
    rpm = args.eqpot_rpm
    rotRate = args.cam_rpm

    # Set initial conditions
    r0 = args.r0
    vr0 = args.vr0
    phi0 = args.phi0
    vphi0 = args.vphi0
