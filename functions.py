def r(t):
    t1 = (((vr0**2)+((r0**2)*(vphi0**2)))*(np.sin(omega*t)**2))/(omega**2)
    t2 = (1/omega)*(r0*vr0*np.sin(2*omega*t))
    t3 = (r0**2)*(np.cos(omega*t)**2)
    return (t1+t2+t3)**(0.5)

def phi(t):
    y = ((1/omega)*(np.sin(omega*t))*(vr0*np.sin(phi0) + r0*vphi0*np.cos(phi0))) + r0*np.sin(phi0)*np.cos(omega*t)
    x = ((1/omega)*(np.sin(omega*t))*(vr0*np.cos(phi0) - r0*vphi0*np.sin(phi0))) + r0*np.cos(phi0)*np.cos(omega*t)
    return np.arctan2(y,x)

def annotate(img, i, rotatingView): # puts diagnostic text info on each frame
    font = cv2.FONT_HERSHEY_TRIPLEX

    dpro = 'SynthPy'
    dproLoc = (25, 50)
    cv2.putText(img, dpro, dproLoc, font, 1, (255,255,255), 1)

    topView = 'Top View'
    topViewLoc = (25, 90)
    cv2.putText(img, topView, topViewLoc, font, 1, (255,255,255), 1)

    if rotatingView:
        rotView = 'Rotating View'
        rotViewLoc = (25, 130)
        cv2.putText(img, rotView, rotViewLoc, font, 1, (55, 255, 90), 1)
    else:
        rotView = 'Inertial View'
        rotViewLoc = (25, 130)
        cv2.putText(img, rotView, rotViewLoc, font, 1, (255, 105, 180), 1)

    img[25:25+spinlab.shape[0], (width-25)-spinlab.shape[1]:width-25] = spinlab

    timestamp = 'Time: ' + str(round((i/fps),1)) + ' s'
    tLoc = (width - 225, height-25)
    cv2.putText(img, timestamp, tLoc, font, 1, (255, 255, 255), 1)

    rad = 'Radius: R = 1 m'
    radLoc = (width -325, height-65)
    cv2.putText(img, rad, radLoc, font, 1, (255, 255, 255), 1)

def parabolaPoints():
    xpoints = np.empty(width)
    ypoints = np.empty(width)
    metersToPixels = float(amp)/2
    for i in range(width):
        if i < (width/2 - int(amp)) or i > (width/2 + int(amp)):
            continue
        xpoints[i] = i
        ypoints[i] = int( ((0.75)*float(fullHeight-height)) - ((omega**2)*((float(i-(width/2))/float(amp))**2)*((metersToPixels)**2))/(2*9.8*metersToPixels))
        nextPoint = np.array([xpoints[i], ypoints[i]])
        try:
            ppoints
        except:
            ppoints = nextPoint
        else:
            ppoints = np.append(ppoints, nextPoint, axis=0)
    return ppoints

def parabola(x):
    metersToPixels = float(amp)/2
    return int( ((0.75)*float(fullHeight-height)) - ((omega**2)*((float(x-(width/2))/float(amp))**2)*((metersToPixels)**2))/(2*9.8*metersToPixels))

def createLineIterator(P1, P2, img):
    """
    Produces and array that consists of the coordinates and intensities of each pixel in a line between two points

    Parameters:
        -P1: a numpy array that consists of the coordinate of the first point (x,y)
        -P2: a numpy array that consists of the coordinate of the second point (x,y)
        -img: the image being processed

    Returns:
        -it: a numpy array that consists of the coordinates and intensities of each pixel in the radii (shape: [numPixels, 3], row = [x,y,intensity])
    """
   #define local variables for readability
    imageH = img.shape[0]
    imageW = img.shape[1]
    P1X = P1[0]
    P1Y = P1[1]
    P2X = P2[0]
    P2Y = P2[1]

   #difference and absolute difference between points
   #used to calculate slope and relative location between points
    dX = P2X - P1X
    dY = P2Y - P1Y
    dXa = np.abs(dX)
    dYa = np.abs(dY)

   #predefine numpy array for output based on distance between points
    itbuffer = np.empty(shape=(np.maximum(dYa,dXa),3))
    itbuffer.fill(np.nan)

   #Obtain coordinates along the line using a form of Bresenham's algorithm
    negY = P1Y > P2Y
    negX = P1X > P2X
    if P1X == P2X: #vertical line segment
        itbuffer[:,0] = P1X
        if negY:
            itbuffer[:,1] = np.arange(P1Y - 1,P1Y - dYa - 1,-1)
        else:
            itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)
    elif P1Y == P2Y: #horizontal line segment
        itbuffer[:,1] = P1Y
        if negX:
            itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
        else:
            itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
    else: #diagonal line segment
        steepSlope = dYa > dXa
        if steepSlope:
            slope = dX.astype(np.float64)/dY.astype(np.float64)
            if negY:
                itbuffer[:,1] = np.arange(P1Y-1,P1Y-dYa-1,-1)
            else:
                itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)
            itbuffer[:,0] = (slope*(itbuffer[:,1]-P1Y)).astype(np.int) + P1X
        else:
            slope = dY.astype(np.float64)/dX.astype(np.float64)
            if negX:
                itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
            else:
                itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
            itbuffer[:,1] = (slope*(itbuffer[:,0]-P1X)).astype(np.int) + P1Y

   #Remove points outside of image
    colX = itbuffer[:,0]
    colY = itbuffer[:,1]
    itbuffer = itbuffer[(colX >= 0) & (colY >=0) & (colX<imageW) & (colY<imageH)]

   #Get intensities from img ndarray
    itbuffer[:,2] = img[itbuffer[:,1].astype(np.uint),itbuffer[:,0].astype(np.uint)]

    return itbuffer


def dottedLine(frame, xi, yi, xf, yf, c1, c2, c3, thickness, segmentLength):
    it = createLineIterator((xi,yi), (xf, yf), frame[:,:,0])
    totLength = (xf-xi)**2 + (yf-yi)**2
    nLines = totLength//segmentLength
    for i in range(nLines):
        if i%2 == 0:
            continue
        #if (i)*segmentLength >= it.shape[0]:
        #    continue
        try:
            cv2.line(frame, (it[i*segmentLength,0], it[i*segmentLength,1]), (it[(i+1)*segmentLength, 0], it[(i+1)*segmentLength, 1]), (c1, c2, c3), thickness)
        except:
            continue

def rotatedDottedLine(theta, frame, xi, yi, xf, yf, c1, c2, c3, thickness, segmentLength):
    centerX = int((xf+xi)/2)
    centerY = int((yf+yi)/2)
    lineRadius = int((((xf-xi)**2 + (yf-yi)**2)**(0.5))/2)
    nXi = int(-lineRadius*np.cos(theta)) + centerX
    nXf = int(lineRadius*np.cos(theta)) + centerX
    nYi = int(lineRadius*np.sin(-theta)) + centerY
    nYf = int(lineRadius*np.sin(theta)) + centerY
    dottedLine(frame, nXi, nYi, nXf, nYf, c1, c2, c3, thickness, segmentLength)

def annotateSideview(img):
    font = cv2.FONT_HERSHEY_TRIPLEX

    dpro = 'Side-View'
    dproLoc = (25, height+borderHeight+25)
    cv2.putText(img, dpro, dproLoc, font, 1, (255,255,255), 1)

    surf = str(rpm) + ' RPM Parabolic Surface'
    surfLoc = (width-500, height+borderHeight+25)
    cv2.putText(img, surf, surfLoc, font, 1, (255,255,255), 1)

    maxDef = ((omega**2))/(2*9.8)
    defl = 'Max. Deflection: h = '+ str(round(maxDef,1)) + ' m'
    deflLoc = (width-500, height+borderHeight+65)
    cv2.putText(img, defl, deflLoc, font, 1, (255,255,255), 1)
