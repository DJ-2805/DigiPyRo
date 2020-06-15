import cv2
import numpy as np


def selection_window(video, dim, start):
    video.set(cv2.CAP_PROP_POS_FRAMES, start)
    ret, frame = video.read()
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_CUBIC)

    cv2.namedWindow('CenterClick')
    cv2.setMouseCallback('CenterClick', center_click)

    while 1:
        cv2.imshow('CenterClick', frame)
        k = cv2.waitKey(0)
        if k == 13:
            break

# User clicks points along the circumference of a circular ROI. This function records the points and calculates the best-fit circle through the points.
def circumferencePoints(event, x, y, flags, param):
    global npts, center, frame, xpoints, ypoints, r, poly1, poly2
    # if user clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # if this is the first point, intialize the arrays of x-y coords
        if (npts == 0):
            xpoints = np.array([x])
            ypoints = np.array([y])
        # otherwise, append the points to the arrays
        else:
            xpoints = np.append(xpoints,x)
            ypoints = np.append(ypoints,y)
        npts+=1
        cv2.circle(frame, (x,y), 3, (0,255,0), -1)
        clone = frame.copy()
        # if there are more than 2 points, calculate the best-fit circle through the points
        if (len(xpoints) > 2):
            bestfit = calc_center(xpoints, ypoints)
            center = (bestfit[0], bestfit[1])
            r = bestfit[2]

            poly1 = np.array([[0,0],
                              [frame.shape[1],0],
                              [frame.shape[1],frame.shape[0]],
                              [0,frame.shape[0]]])

            poly2 = np.array([[bestfit[0]+r,
                               bestfit[1]]])
            circpts = 100
            # approximate the circle as a 100-gon
            # which makes it easier to draw the mask,
            # as we define the mask region as the area between two polygons
            for i in range(1,circpts):
                theta =  2 * np.pi * (i / circpts)
                nextpt = np.array([[int(bestfit[0] + (r * np.cos(theta))),
                                    int(bestfit[1] + (r * np.sin(theta)))]])
                poly2 = np.append(poly2, nextpt, axis=0)

            cv2.circle(frame, center, 4, (255,0,0), -1)
            cv2.circle(frame, center, r, (0,255,0), 1)

        cv2.imshow('CenterClick', frame)
        frame = clone.copy()

def calc_center(xp, yp):
    n = len(xp)
    xp2 = xp**2
    yp2 = yp**2
    xy = xp * yp

    circleArr = np.array([[np.sum(xp2), np.sum(xy), np.sum(xp)],
                          [np.sum(xy), np.sum(yp2), np.sum(yp)],
                          [np.sum(xp), np.sum(yp), n]])

    circleVec = np.array([np.sum(xp * (xp2 + yp2)),
                          np.sum(yp * (xp2 + yp2)),
                          np.sum(xp2 + yp2)])

    circleInv = np.linalg.inv(circleArr)

    M = np.dot(circleInv, circleVec).T

    xc = M[0] / 2
    yc = M[1] / 2
    d = M[0]**2 + M[1]**2 + M[2] * 4
    diam = np.sqrt(d)
    return np.array([int(xc), int(yc), int(diam / 2)])


# ####################################################
    circleMatrix = np.matrix([[np.sum(xp**2), np.sum(xp*yp), np.sum(xp)],
                              [np.sum(xp*yp), np.sum(yp**2), np.sum(yp)],
                              [np.sum(xp), np.sum(yp), n]])
    circleVec = np.transpose(np.array([np.sum(xp*((xp**2)+(yp**2))), np.sum(yp*((xp**2)+(yp**2))), np.sum((xp**2)+(yp**2))]))
    ABC = np.transpose(np.dot(np.linalg.inv(circleMatrix), circleVec))
    xc = ABC.item(0)/2
    yc = ABC.item(1)/2
    a = ABC.item(0)
    b = ABC.item(1)
    c = ABC.item(2)
    d = (4*c)+(a**2)+(b**2)
    diam = d**(0.5)
    return np.array([int(xc), int(yc), int(diam/2)])
